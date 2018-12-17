#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
import json
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()

def getHtml(url):
	global cookie
	try:
		response = requests.get(url)
	except:
		return ''
	else:
		return response.content

def analyzeHtml(html, p, encode = True):
	pattern = re.compile(p)
	if encode:
		return pattern.findall(html.decode('gbk').encode('utf-8'))
	else:
		return pattern.findall(html)
		

def analyzeUrl(url, p):
	html = getHtml(url)
	return analyzeHtml(html, p)
	#pattern = re.compile(p)
	#return pattern.findall(html.decode('gbk').encode('utf-8'))

def spiderAbout(r):
	url = 'http://' + r[1] + '.pp.163.com/about/'
	#url = 'http://dddex.pp.163.com/'
	html = getHtml(url)
	about = analyzeHtml(html, r'<h4>.*?<span class="f-ml5 simsun" id="p_home_rank"></span>(.*?)</h4>')
	cameras = analyzeHtml(html, r'<p class="data-item"> <b class="w-icoCamero data-ico">相机.*?</p>')
	cameras = analyzeHtml('' if len(cameras) == 0  else cameras[0], r'<em>(.*?)</em>', False)
	lenses = analyzeHtml(html, r'<p class="data-item"> <b class="w-icoBrand data-ico">镜头.*?</p>')
	lenses = analyzeHtml('' if len(lenses) == 0 else lenses[0], r'<em>(.*?)</em>', False)
	preference = analyzeHtml(html, r'偏好：</div> </div> <div class="colum colum-400"> <div class="line">(.*?)</div>')
	about = '' if len(about) == 0 else about[0]
	cameras = '' if len(cameras) == 0 else ','.join(cameras)
	lenses = '' if len(lenses) == 0 else ','.join(lenses)
	preference = '' if len(preference) == 0 else preference[0]
	print r,about,cameras,lenses,preference
	#sendMessage(r[3],r[4])
	exit()

def sendMessage(uname, userId):
	url = 'http://photo.163.com/share/' + uname +  '/dwr/call/plaincall/ShareMessageBean.addShareMessage.dwr'
	#payload = 'callCount=1\nscriptSessionId=${scriptSessionId}187\nc0-scriptName=ShareMessageBean\nc0-methodName=addShareMessage\nc0-id=0\nc0-param0=string:' + userId  + '\nc0-param1=number:0\nc0-param2=string:%E6%82%A8%E5%A5%BD%EF%BC%81%E6%88%91%E6%98%AF%E3%80%8A%E6%95%B0%E7%A0%81%E4%B8%96%E7%95%8C%E3%80%8B%E6%9D%82%E5%BF%97%E6%91%84%E5%BD%B1%E4%B8%93%E6%A0%8F%E5%BE%90%E6%95%8F%EF%BC%8C15810683299%E5%90%8C%E5%BE%AE%E4%BF%A1%EF%BC%8C%E6%AC%A2%E8%BF%8E%E6%82%A8%E7%9A%84%E6%91%84%E5%BD%B1%E4%BD%9C%E5%93%81%E6%9D%A5%E6%88%91%E4%BB%AC%E6%9D%82%E5%BF%97%E5%88%8A%E7%99%BB%E5%8F%91%E8%A1%A8%E3%80%81%E5%81%9A%E4%B8%93%E6%A0%8F%E3%80%81%E4%B8%93%E8%AE%BF%EF%BC%81%E6%88%91%E4%BB%AC%E6%9D%82%E5%BF%97%E6%AD%A3%E5%9C%A8%E5%9B%9E%E9%A6%88%E6%91%84%E5%BD%B1%E4%BA%BA%EF%BC%8C%E9%82%80%E8%AF%B7%E6%82%A8%E5%8F%82%E5%8A%A02018%E5%B9%B4%E4%BC%98%E7%A7%80%E4%BD%9C%E5%93%81%E5%B1%95%E7%A4%BA%EF%BC%88%E5%A4%8F%E5%AD%A3%E8%B5%9B%EF%BC%89%E8%AF%84%E9%80%89%E5%A4%A7%E8%B5%9B%E3%80%82%E5%8F%A6%E5%BC%80%E8%BE%9F%E4%BA%86%E7%94%84%E9%80%89%E7%89%B9%E7%BA%A6%E6%91%84%E5%BD%B1%E5%B8%88%2B%E7%94%B3%E5%8A%9E%E6%91%84%E5%BD%B1%E9%87%87%E8%AE%BF%E8%AF%81%E6%B4%BB%E5%8A%A8%EF%BC%81%E7%9C%9F%E8%AF%9A%E9%82%80%E8%AF%B7%E6%82%A8%E7%9A%84%E5%8F%82%E5%8A%A0%EF%BC%81\nbatchId=967336'
	payload = 'callCount=1\nscriptSessionId=${scriptSessionId}187\nc0-scriptName=ShareMessageBean\nc0-methodName=addShareMessage\nc0-id=0\nc0-param0=string:' + userId  + '\nc0-param1=number:0\nc0-param2=string:spider send message\nbatchId=967336'
	headers = {'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':str(len(payload)),
	'Content-Type':'text/plain',
	'Cookie':'vjuids=12f4ed5b1.15c49e82224.0.099b93e39828b; _ntes_nnid=29cb965f0cf71ee2de9ea5d407767e11,1495888568890; _ntes_nuid=29cb965f0cf71ee2de9ea5d407767e11; usertrack=ZUcIhllh6QWHgwIWQEKzAg==; NTES_REPLY_NICKNAME=zhiqiuyiye2564%40163.com%7Czhiqiuyiye2564%7C2157165976923906739%7Czhiqiuyiye2564%7Chttp%3A%2F%2Fimgm.ph.126.net%2FpLnp5B1G4d7H1pDrNCworg%3D%3D%2F3255258105758749723.jpg%7CqKu5jss8uSmhlZhmFPZFghFi56zzB5FfGugiiAToHb7uS5ZthCvlJcQCLw982FSlADiZIVNEYZJAglEc7eOB0USmYuqdBL0PyPH2_k7PR2r0mtrRDTXhhYirieNGlwdR8%7C1%7C2; mp_MA-B4F0-3EDB3213C01D_hubble=%7B%22deviceUdid%22%3A%20%22f32c787c-ec41-4f35-a497-73c0d6fafa1d%22%2C%22updatedTime%22%3A%201510759850701%2C%22sessionStartTime%22%3A%201510759850701%2C%22sessionReferrer%22%3A%20%22http%3A%2F%2Fwww.163.com%2F%22%2C%22sessionUuid%22%3A%20%220f42284f-6c74-4c08-ade1-c1bb2d777f09%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fwww.163.com%2F%22%2C%22initial_referring_domain%22%3A%20%22www.163.com%22%2C%22persistedTime%22%3A%201510759850701%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201510759850713%7D%7D; __oc_uuid=0a530600-d1d2-11e7-b836-e713fe55c0ee; NTES_CMT_USER_INFO=523311%7C%E6%AF%9B%E7%91%9FC96%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F763007e09b964f60aeec4aadc6e10f4920170612162127.jpg%7Ctrue%7CemhpcWl1eWl5ZTI1NjRAMTYzLmNvbQ%3D%3D; _ngd_tid=TVS%2F%2Br1eZ%2BpeWDgSw7BCv5I%2FFqTiXPno; __e_=1525230887034; vinfo_n_f_l_n3=b69bd3f7f7a48f81.1.108.1495888585738.1525181854961.1525358958316; mail_psc_fingerprint=be0bbb0a944b6d2e846cd131eeb5a0ff; __f_=1525826966181; NETEASE_AUTH_USERNAME=dgtspace99; __utma=187553192.1593254579.1499588880.1525784169.1525881292.4; __utmc=187553192; __utmz=187553192.1525881292.4.4.utmcsr=reg.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/Main.jsp; NNSSPID=0a93df79c16540d6b4decf00c62faf9d; starttime=; nts_mail_user=13641254663@163.com:-1:1; df=mail163_letter; Province=010; City=010; USERTRACK=111.194.47.58.1526133520857646; uid=ezq0VFr281SkfSyzHNJUAg==; JSESSIONID-WYXC=7f2f37cc2ee4ba1017b1317f23d405445a75f96a6d6eca84f791f69d683de5aa51a5b00f0e8f825b4859397660d892b90193911fbe9782c2aa4508fb27ea511339415a7ea298a83a14f0462d6c6bdd5824cfd400ee238847d863eb0157d8605695f89194f1740316e9ac690320dff30b9104a544713ee69765a65c1469c8d787553e4d3d; ALBUMAPPID=252AE6515FD318379C7E0F42C1AA7F2C.cloudphoto61-8011; NEPHOTO_LOGIN=; NTES_hp_textlink1=old; vjlast=1495888569.1526173549.11; NTES_SESS=4XlZOJDEqqpXwvw9ZF0nIRT6D7ieIGbolcQ2i0YOgXy768YH69PjrG9OJBVjEgpL5JxPo.mosw6obuI3djqtp5nI5rFpBjMccwfsTDXv3FF__wdnQ8ZZJABAzjHvsVGA34Gzj3JERy3sh7uee8hxH9omvrjtwW4dJaMGXZIM7F.dRTAAvAXUtWrKHV0jIDuDIwLTjDDA1ZBnG; S_INFO=1526215449|0|2&70##|qq3348447708; P_INFO=qq3348447708@163.com|1526215449|0|blog|00&99|bej&1526133900&blog#bej&null#10#0#0|&0|urs&blog|qq3348447708@163.com; ALBUMSHAREID=299EB4BA4861204AA13170FC1EC3ACE8.classa-webshare3-8015; _ga=GA1.2.1593254579.1499588880; _gid=GA1.2.1217939378.1526133523',
	'Host':'photo.163.com',
	'Origin':'http://photo.163.com',
	'Referer':'http://photo.163.com/crossdomain.html?t=20100205',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'} 
	print json.dumps(payload)
	r = requests.post(url, data=payload, headers=headers)
	print r.content

def run():
	sendMessage('zhiqiuyiye2564', '25319003')
	exit()
	global cur,conn
	maxPage = 2 #500
	for page in range(maxPage):
		url = 'http://photo.163.com/share/qq3348447708/dwr/call/plaincall/PictureSetBean.getPictureSetHotListByDirId.dwr?callCount=1&scriptSessionId=%24%7BscriptSessionId%7D187&c0-scriptName=PictureSetBean&c0-methodName=getPictureSetHotListByDirId&c0-id=0&c0-param0=number%3A-1&c0-param1=number%3A' + str(page * 20) + '&c0-param2=number%3A20&c0-param3=string%3AWeightAll&c0-param4=number%3A1&c0-param5=string%3AShareSet&batchId=562293'
		result = analyzeUrl(url, r'city="(.*?)";.+domainName="(.+?)";.+nname="(.+?)";.+uname="(.+?)";.+userId=(.+?);')
		print result
		exit()
		for r in result:
			spiderAbout(r)


conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

run()

cur.close()
conn.close()
