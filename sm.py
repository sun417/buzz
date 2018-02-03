#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
import time
import json
from lxml import html
from var_dump import var_dump

offset = sys.argv[1]
limit = sys.argv[2]

cookie = {}
raw_cookies = '_hideMessageTips=1; visitor_flag=1512054951; visitor_r=; cmt_hash=1874997032; _topbar_introduction=1; lastphoto_show_mode=list; session_id=d9fa888e7e3e8d0b622ff7d70cb0348b; world_user_login=1; session_ip=111.194.49.82; session_ip_location=101001001; ams_eyes=1; session_auth_hash=cf9987e391c2d407eff34d53cd537a94; visitor_b=mypoco.css; visitor_l=poco_tj.css; _topbar_inducement_app=1; _topbar_inducement_community=1; g_session_id=d2efc69d914d4ff291f4e840b2f428e8; member_id=188504872; fav_userid=188504872; remember_userid=188504872; nickname=POCO%CA%D6%BB%FA%D3%C3%BB%A7; fav_username=POCO%CA%D6%BB%FA%D3%C3%BB%A7; activity_level=new; pass_hash=d2bc2f8d09990ebe87c809684fd78c66'
for line in raw_cookies.split(';'):
    key,value = line.split("=", 1)
    cookie[key] = value

text = '您好！我是《数码世界》杂志摄影专栏徐敏，15810683299同微信，欢迎您的摄影作品来我们杂志刊登发表！来我们杂志做专栏、专访！我们杂志正在回馈摄影人，凡是在2018年3月前刊登作品的作者，可以参加2017年度摄影大奖评审!真诚邀请您的参加！'
url = 'http://my.poco.cn/m/ajax/message/add.php'

conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

result = cur.execute("select id,user_id from spider_log order by id limit %s, %s" % (offset, limit))
rows = cur.fetchmany(result)
for row in rows:
	rid,uid = row
	print rid,uid
	try:
		data = {'uid':uid, 'text':text}
		response = requests.post(url, cookies=cookie, data=data)
	except Exception, e:
		print e.message
	else:
		r = json.loads(response.text)
		print r
		#var_dump(r)
		print rid, uid, response.text	
	
	time.sleep(60)

cur.close()
conn.close()
