const crawler = require("crawler")
const readlineSync = require("readline-sync")
const mysql = require('mysql')
const cheerio = require('cheerio')
const fs = require('fs')
const path = require("path")
const request = require('request')
require("string-format").extend(String.prototype)

const config = require("./website.json")

//const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

class Spider {
    constructor(){
        this.existCount = 0
        this.c = new crawler({
            maxConnections: 1,
            rateLimit: 5000,
            retryTimeout: 5000,
            retries: 3,
            normalizeWhitespace: false,
            xmlMode: false,
            decodeEntities: true,
            preRequest: function(options, done) {
                console.log("正在爬取：", options.uri)
                done()
            }
        })

        this.connection = mysql.createConnection({
              host     : '127.0.0.1',
              user     : 'root',
              password : '123123',
              database : 'yzmcms'
        })
        
        this.connection.connect()
    }

    getResponse(uri, isDownload = false){
		let that = this
		return new Promise(function(resolve, reject){
            if(isDownload){
                that.c.direct({
                    uri,
                    callback: function(err, res){
                        if(err != null){
                            reject(err)
                        } else {
                            resolve(res)
                        }
                    }
                })
            } else{
                that.c.queue({
                    uri : uri,
                    callback: function(err,res, done){
                        done()
                        if(err != null){
                            reject(err)
                        } else {                            
                            let $ = cheerio.load(res.body, {decodeEntities: false})
                            resolve($)
                        }
                    }	
                })
            }
		})
    }

    query(sql, params){
        let that = this
        return new Promise(function(resolve, reject){
            that.connection.query(sql, params, function(err, res){
                if(err != null){
                    return reject(err)
                } else {                    
                    return resolve(res)
                }
            })
        })
    }

    async getMaxPage(){
        try{
            let $ = await this.getResponse(this.siteConfig.BaseUrl.format(1))
            let maxPage = parseInt($(this.siteConfig.PageSelector).text())
            if(!maxPage){
                maxPage = 1
            }
            return maxPage
        } catch(err){
            console.log("抓取 Max Page 异常：", err)
            process.exit()
        }
    }

    async getList(maxPage) {
        try{
            for(let page = 1; page <= maxPage; page++) {
                let $ = await this.getResponse(this.siteConfig.BaseUrl.format(page))
                $(this.siteConfig.ListSelector).each(async (index, item) => {
                    let url = item.attribs.href
                    if(!(url.startsWith('http://') || url.startsWith('https://'))){
                        url = this.siteConfig.Url + url
                    }
                    //console.log(url)
                    await this.getMeeting(url)
                })
            }
        } catch(err){
            console.log("抓取 文章列表 异常：", err)
        }
    }

    async getMeeting(url){
        url = 'https://www.huodongjia.com//event-1723507090.html'
        let that = this
        try{
            let $ = await this.getResponse(url)
            let mettingTitle = $(this.siteConfig.MeetingTitleSelector).text()
            console.log(mettingTitle)
            let isExist = await this.isExistMeeting(mettingTitle)
            if(isExist){
                this.existCount++
                if(this.existCount >= 3){
                    console.log("列表已重复爬取，结束")
                    process.exit()
                }
            } else {
                this.existCount = 0
                let meetingContent = $(this.siteConfig.MeetingContentSelector).html()
                if(this.siteConfig.UpdateImage){
                    let imgs = $(this.siteConfig.MeetingContentSelector + ' img')
                    console.log(imgs.length)
                    for(let i = 0; i < imgs.length; i++){
                        let res = await this.downloadImage(imgs[i].attribs.src)
                    }
                    // $(this.siteConfig.MeetingContentSelector + ' img').each(async(index, item) => {
                    //     await that.downloadImage(item.attribs.src)
                    // })
                }
                process.exit()
                let meetingDate = $(this.siteConfig.MeetingDateSelector).text()
                let meetingOpenDate = new Date(meetingDate.match(this.siteConfig.MeetingOpenDateRegx)[1]).getTime() / 1000
                let meetingEndDate = new Date(meetingDate.match(this.siteConfig.MeetingEndDateRegx)[1]).getTime() / 1000
                let meetingPlace = $(this.siteConfig.MeetingPlaceSelector).text()
                let meetingCity = meetingPlace.match(this.siteConfig.MeetingPlaceRegx)[1]
                let meetingDescription = $(meetingContent).text().trimStart().substring(0,100) + "..."
                let inputTime = parseInt(new Date().getTime() / 1000)
                let params = [mettingTitle,mettingTitle+'_医学会议网',meetingCity,meetingOpenDate,meetingEndDate,
                    inputTime,inputTime,meetingDescription,meetingContent]
                // let result = await this.insert(params)
                // if(!result.insertId){
                //     console.log("文章入库 异常：", result.message)
                //     return
                // }
            }
        } catch(err){
            console.log("抓取 文章 异常：", err)
            console.log(url)
        }
    }

    async downloadImage(url){
        console.log(url)
        let now = new Date()
        let fullYear = now.getFullYear()
        let shortYear = fullYear.toString().substr(2)
        let month = (now.getMonth() + 1).toString().padStart(2,'0')
        let day = now.getDate()
        let hour = now.getHours()
        let minute = now.getMinutes()
        let second = now.getSeconds()
        let random = Math.floor((Math.random() * 1000) + 1)
        let ext = url.split('.').pop()
        let fileName = `${shortYear}${month}${day}${hour}${minute}${second}${random}.${ext}`
        let path = `./uploads/${fullYear}${month}/${day}/`
        this.mkdirsSync(path)
        // fs.exists(path, (exists) => {
        //     if(!exists){
        //         fs.mkdir(path, { recursive: true }, (err) => {
        //             if (err) throw err;
        //           });
        //     }
        // });
        console.log(path)
        // request({url}).pipe(fs.createWriteStream(`./images/${fileName}`).on('close',err=>{  console.log('写入失败',err) }))
        // await request(url, async(error, response, body) => {
        //     if(!error && response.statusCode == 200){
        //         console.log(body)
        //     } else {
        //         console.log(error)
        //     }
        // })
        let res = await this.getResponse(url, true)
        //console.log(res.body)
    }

    async isExistMeeting(title){
        try{
            let sql = 'Select Count(1) As Count From yzm_article Where title=?'
            let params = [title]
            let result = await this.query(sql, params)
            return result[0].Count !== 0
        } catch(err){
            console.log("数据库操作异常：", err)
        }
    }

    async insert(params){
        try{            
            let sql = `Insert yzm_article (catid,userid,username,nickname,title,seo_title,city,begintime,endtime,inputtime,updatetime,description,content,status) 
            Values(1,1,'admin','管理员',?,?,?,?,?,?,?,?,?,0)`
            let result = await this.query(sql, params)
            return result
        } catch(err){
            console.log("插入记录异常：", err)
        }
    }

    mkdirsSync(dirname) {
        if (fs.existsSync(dirname)) {
          return true;
        } else {
          if (this.mkdirsSync(path.dirname(dirname))) {
            fs.mkdirSync(dirname);
            return true;
          }
        }
    }

    async crawling(){
        let maxPage = await this.getMaxPage()
        this.getList(maxPage)
    }

    run(){
        // this.siteConfig = config[0]
        config.forEach((site, index) => {
            console.log("%d. %s", index + 1, site.SiteName)
        })
        let choice = parseInt(readlineSync.question('请选择爬取的站点：'))
        if(!choice || choice < 0 || choice > config.length){
            console.log("选择错误！")
            process.exit()
        }
        this.siteConfig = config[choice - 1]
        
        this.crawling()
    }
}

const spider = new Spider()
spider.run()
