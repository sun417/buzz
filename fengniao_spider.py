#-*-coding:utf-8-*-
import re
import pymysql
import requests
from bs4 import BeautifulSoup
import json
import time


def getHost(url):
	return 'my.fengniao.com' if url.__contains__('my.fengniao') else 'bbs.fengniao.com'

def getJson(url, param):
	headers['Host'] = getHost(url)
	# data = getData(param)
	response = requests.post(url, headers=headers, data=param)
	resultJson = json.loads(response.text)
	return resultJson

def analyzeText(text, p):
	pattern = re.compile(p)
	return pattern.findall(text)

def getHtml(url):
	headers['Host'] = getHost(url)
	try:
		response = requests.get(url, headers=headers)
	except:
		return None
	else:
		bs = BeautifulSoup(response.content, 'html.parser')
	return bs

def run(uid, current_crawl_deep):
	try:
		global cur, conn, uidList
		if uid in uidList:
			return
		uidList.append(uid)
		sql = "select id from fengniao where user_id=%d" % uid
		count = cur.execute(sql)
		conn.commit()
		if count != 0:
			return
		current_crawl_deep += 1
		url = 'https://my.fengniao.com/index.php?userid=%d' % uid
		bsObj = getHtml(url)
		if bsObj == None:
			print("%d 的获取作品数量失败" % uid)
			return
		e = bsObj.select('h4.tit')
		if len(e) == 0:
			return
		result = analyzeText(e[0].get_text(), '\d+')
		if len(result) == 0:
			return
		album_count = int(result[0]) #作品数量

		if album_count == 0 :
			return

		url = 'https://my.fengniao.com/info.php?userid=%d' % uid
		bsObj = getHtml(url)
		if bsObj == None:
			return
		e = bsObj.select('ul.dataList span.txt')
		if e == None:
			return
		user_name = e[0].get_text()
		gender = 0 if e[1].get_text() == u'未知' else 1 if e[1].get_text() == u'男' else 2
		city = e[2].get_text()
		sign = e[3].get_text()
		reg_date = e[4].get_text() 
		weibo = e[5].get_text()
		qq = e[6].get_text()
		email = qq + '@qq.com' if qq != u'暂无' else ''	
		
	
		e =  bsObj.select('.liBox .txt')
		if e == None:
			return
		fans_count = e[0].get_text()
		follow_count = e[1].get_text()
		level = e[2].get_text()
		e = bsObj.select('.personalInfor .nameLabel')
		fengniao_level = e[0].get_text()

		url = 'https://my.fengniao.com/ajax/ajaxGetListsInfo.php'
		param = {
			"from":"getZuoPinLists",
			"type":1,
			"page":1,
			"userId":uid,
			"fromType":"index"
			}
		json = getJson(url, param)

		if json['code'] != 1:
			return
		url = ''
		for li in json['data']:
			if type(li).__name__ != 'dict':
				continue
			if int(li['type']) == 1:
				url = li['jumpUrl']
				break
		bsObj = getHtml(url)
		if bsObj == None:
			return

		e = bsObj.select('.peopleTxt span')
		score = e[0].get_text()[3:]

		camera_brand = ''
		camera_type = ''
		camera_lens_brand = ''
		camera_lens_type = ''
		e = bsObj.select('.postList')
		if len(e) > 0 :
			e = e[0].select('.exifBox span')		
			if len(e) != 0:
				camera_brand = e[0].get_text()
				camera_type = e[1].get_text()

			if len(e) > 8:
				camera_lens_brand = e[7].get_text()
				camera_lens_type = e[8].get_text()

		sql = "INSERT INTO fengniao (user_id,user_name,city,email,qq,gender,weibo,sign,reg_date,level,fengniao_level,score,album_count,fans_count,follow_count,camera_brand,camera_type,camera_lens_brand,camera_lens_type) VALUES (%d,'%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s','%s','%s','%s')" % (uid,user_name,city,email,qq,gender,weibo,sign,reg_date,level,fengniao_level,score,album_count,fans_count,follow_count,camera_brand,camera_type,camera_lens_brand,camera_lens_type)

		#print(sql)
		
		cur.execute(sql)
		conn.commit()
		print('%d - %s' % (uid, user_name.encode('utf8')))
		time.sleep(5)
	except Exception as e:
		print('%d - %s - %s' % (uid, user_name.encode('utf8'), e))
		pass

	if current_crawl_deep > 7:
		return


# 	#解析好友
	p = 1
	url = 'https://my.fengniao.com/friend.php?action=friend&userid=%d&page=%d' % (uid, p)
	bsObj = getHtml(url)
	e = bsObj.select('.page span')
	totalCount = 1
	if len(e) > 0:
		totalCount = int(analyzeText(e[0].get_text(), '\d+')[0])
	while p <= totalCount:
		url = 'https://my.fengniao.com/friend.php?action=friend&userid=%d&page=%d' % (uid, p)
		bsObj = getHtml(url)
		uids = bsObj.select('.FriendsList li .followBtn')
		if len(uids) == 0:
			return
		for user in uids:
			run(int(user.attrs['uid']), current_crawl_deep)
		p += 1

def getUidList():
	global cur, conn
	uidList = []
	sql = 'select distinct user_id from fengniao'
	cur.execute(sql)
	uidTuple = cur.fetchall()
	for uid in uidTuple:
		uidList.append(uid[0])
	return uidList

conn = None
cur = None
uidList = []
headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'ip_ck=7saB4P32j7QuOTEwNzcxLjE1NDc5NTM3OTY%3D; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1558367322; bbuserid=11124656; bbpassword=96a533352aecd403ca4fd164325565dd; bbusername=FNYX11124656; lv=1560697761; vn=13; Adshow=1; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1560698582',
	'Host': 'my.fengniao.com',
	'Referer': 'https://my.fengniao.com/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
}

def main():
	global  conn, cur, uidList
	conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='123123', db='spider', charset='utf8')
	cur = conn.cursor()
	uidList = getUidList()
	# seed_id = 156286# 种子url
	seed_id = 1187735# 种子url
	#seedid = 10437722
	run(seed_id, 0)
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()
