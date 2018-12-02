#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
import time
import md5
import json
from lxml import html
from var_dump import var_dump

offset = sys.argv[1]
limit = sys.argv[2]

def getHtml(url):
	global headers
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
	"Cookie":"last_ad_popup=0; last_hit_ad=0; my.register=tf844; my.register.flag=43650; JSESSIONID=abcsuuE9vlxAjhpZcIGrw; lastvisit=1530628115937; uid=8a2b978a644bdc1e0164608b8c6e0ebf; pwd=4f5f3c2adbcc8752f1e2e4b81ea188c4; rm=null; sid=8a2b978a645dd0af0164608b8ddd013c; reminder=1530629398513%2C0%7C0",
}


text = '您好！我是《数码世界》杂志摄影专栏徐敏，15810683299同微信，欢迎您的摄影作品来我们杂志刊登发表、做专栏、专访！我们杂志正在回馈摄影人，邀请您参加2018年优秀作品展示（夏季赛）评选大赛。另开辟了甄选特约摄影师+申办摄影采访证活动！真诚邀请您的参加！'
url = 'http://my.nphoto.net/message_send/post'

conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
cur = conn.cursor()

result = cur.execute("select id,user_id,name from nphoto order by lastlogin desc limit %s, %s" % (offset, limit))
rows = cur.fetchmany(result)
#rows = [{'27991','jiuyue_robin','九月robin'}]
for row in rows:
	rid,uid,name = row
	name = name.encode('utf8')
	print rid,uid,name
	#continue
	#exit()
	try:
		result = analyzeHtml('http://my.nphoto.net/message_write/%s' % uid, r'<input type="hidden" name="userid" value="(.+?)">')
		if len(result) == 0:
			print offset,rid,uid,name,'userid获取失败'
			exit()
		userid = result[0]
		data = {
			'subject':name + '您好',
			'message':name + text,
			'userid':userid,
			'action':''
		}
		response = requests.post(url, headers = headers, data = data)
		print offset,rid,uid,name,'send ok'
		offset = int(offset) + 1
		time.sleep(300)
	except Exception, e:
		print 'error'
		print e.message 
		exit()

cur.close()
conn.close()
