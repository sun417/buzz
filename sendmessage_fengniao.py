#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
import time
import md5
import json
import random
import traceback
from lxml import html
from var_dump import var_dump

offset = sys.argv[1]
limit = sys.argv[2]

cookie = {}
raw_cookies = 'ip_ck=5MOD7/L3j7QuMzQyODgwLjE1MTc3NTI1OTI%3D; lv=1517752592; vn=1; PHPSESSID=5cqk208is870c3gm2aat511d82; Adshow=4; loginRefer=http%3A%2F%2Fmy.fengniao.com%2F; bbuserid=10803486; bbpassword=40fa28fae8e4f527130982b9b8b02dd3; bbusername=%E6%95%B0%E7%A0%81%E4%B8%96%E7%95%8C%E5%BE%90%E6%95%8F; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1517750378,1518396757; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1519140913'
for line in raw_cookies.split(';'):
	key,value = line.split("=", 1)
	cookie[key] = value

message = '您好！我是《数码世界》杂志摄影专栏徐敏，15810683299同微信，欢迎您的摄影作品来我们杂志刊登发表、做专栏、专访！我们杂志正在回馈摄影人，邀请您参加由中国新時代摄影家协会 、《数码世界》杂志社主办的首届“著名摄影师”暨“优秀摄影师”评选！'
url = 'https://my.fengniao.com/ajax/ajaxMessage.php'

conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

result = cur.execute("select id,user_id,nickname from fengniao_log order by id limit %s, %s" % (offset, limit))
rows = cur.fetchmany(result)
count = int(offset)
for row in rows:
	rid,uid,nickname = row
	try:
		text = nickname + message
		print text
		data = {'f_userid':uid,'nickname':nickname,'invite_content':text,'action':'sendMessage'}

		while True:
			response = requests.post(url, cookies=cookie, data=data)
			resultJson = json.loads(response.text)
			if resultJson['code'] == 1:
				msg = resultJson['msg'].encode('utf8')
				print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " ", count, ":", rid, uid, msg
				time.sleep(20)
				break
			else:
				print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count, ":", rid, uid, resultJson['code'], resultJson['msg'].encode('utf8')
				if resultJson['code'] == -9:
					print "休眠12小时"
					time.sleep(12 * 60 * 60)

		count = count + 1
	except Exception, e:
		pass

cur.close()
conn.close()
