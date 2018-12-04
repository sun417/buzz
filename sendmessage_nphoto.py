#-*-coding:utf-8-*-
import sys
import requests
import re
# import MySQLdb
import time
# import md5
import json
# from lxml import html
# from var_dump import var_dump

offset = 1#sys.argv[1]
limit = 1#sys.argv[2]

def getHtml(url):
	global headers
	# print(headers)
	# exit()
	try:
		response = requests.get(url, headers = headers)
	except:
		print(e.message)
		return ''
	else:
		return response.content

def analyzeHtml(url, p):
	html = getHtml(url)
	pattern = re.compile(p)
	return pattern.findall(html)

headers = {
	"Host":"my.nphoto.net",
	"Connection":"keep-alive",
	# "Content-Length":"86",
	"Cache-Control":"max-age=0",
	# "Origin:http":"//my.nphoto.net",
	"Upgrade-Insecure-Requests":"1",
	"Content-Type":"application/x-www-form-urlencoded",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8123123",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"zh-CN,zh;q=0.9",
	"Cookie":"JSESSIONID=abcwm23KkINX14RPnPDqw; lastvisit=1529752413068; last_ad_popup=0; last_hit_ad=0; uid=8a2b978a63dc50cd0164133e11eb21e8; pwd=4f5f3c2adbcc8752f1e2e4b81ea188c4; sid=8a2b978a63dc50cd01642c596389325b; rm=1",
}


text = '您好！我是《数码世界》杂志摄影专栏徐敏，15810683299同微信，欢迎您的摄影作品来我们杂志刊登发表、做专栏、专访！我们杂志正在回馈摄影人，邀请您参加2018年优秀作品展示（夏季赛）评选大赛。另开辟了甄选特约摄影师+申办摄影采访证活动！真诚邀请您的参加！'
url = 'http://my.nphoto.net/message_send/post'

# conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
# cur = conn.cursor()
#
# result = cur.execute("select id,user_id,name from nphoto order by lastlogin desc limit %s, %s" % (offset, limit))
# rows = cur.fetchmany(result)
rows = [{'27991','np326054845','江河源'}]
for row in rows:
	#rid = row[0]
	#uid = row[1]
	rid,uid,name = row
	#print rid,uid
	#exit()
	try:
		result = analyzeHtml('http://my.nphoto.net/message_write/%s' % uid, r'<input type="hidden" name="userid" value="(.+?)">')
		print(result)
		# param = '{"thread_id":"","action":4,"content":"%s","receiver_user_id":"%s","target_type":3,"user_id":188535207,"access_token":"2811521866772316641"}' % (text, uid)
		# plant = 'poco_%s_app' % param
		# m1 = md5.new()
		# m1.update(plant)
		# m5 = m1.hexdigest()
		# sign_code = m5[5:5+19]
		# ctime = int(round(time.time() * 1000))
		# req = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":%d,"param":%s,"sign_code":"%s"}' % (ctime, param, sign_code)
		# data = {'host_port':'http://my.poco.cn', 'req':req}
		# response = requests.post(url, cookies=cookie, data=data)
		# resultJson = json.loads(response.text)
		# if resultJson['code'] == 10000:
		# 	message = resultJson['message'].encode('utf8')
		# 	print rid, uid, message
		# else:
		# 	print rid, uid, response.text
		# time.sleep(180)
	except Exception as e:
		print(e.message)

# cur.close()
# conn.close()
