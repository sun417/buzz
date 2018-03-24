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

cookie = {}
raw_cookies = '_hideMessageTips=1; visitor_flag=1512054951; visitor_r=; cmt_hash=1874997032; _topbar_introduction=1; lastphoto_show_mode=list; session_id=d9fa888e7e3e8d0b622ff7d70cb0348b; world_user_login=1; session_ip=111.194.49.82; session_ip_location=101001001; ams_eyes=1; session_auth_hash=cf9987e391c2d407eff34d53cd537a94; visitor_b=mypoco.css; visitor_l=poco_tj.css; _topbar_inducement_app=1; _topbar_inducement_community=1; g_session_id=d2efc69d914d4ff291f4e840b2f428e8; member_id=188504872; fav_userid=188504872; remember_userid=188504872; nickname=POCO%CA%D6%BB%FA%D3%C3%BB%A7; fav_username=POCO%CA%D6%BB%FA%D3%C3%BB%A7; activity_level=new; pass_hash=d2bc2f8d09990ebe87c809684fd78c66'
for line in raw_cookies.split(';'):
    key,value = line.split("=", 1)
    cookie[key] = value

text = '您好！我是《数码世界》杂志摄影专栏徐敏，15810683299同微信，欢迎您的摄影作品来我们杂志刊登发表、做专栏、专访！我们杂志正在回馈摄影人，邀请您参加迎2018年新春杯摄影大赛。另开辟了甄选特约摄影师+申办摄影采访证活动！真诚邀请您的参加！'
url = 'http://web-api.poco.cn/v1_1/message/create_notify'

conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
cur = conn.cursor()

result = cur.execute("select id,user_id from spider_log order by id limit %s, %s" % (offset, limit))
rows = cur.fetchmany(result)
for row in rows:
	#rid = row[0]
	#uid = row[1]
	rid,uid = row
	#print rid,uid
	#exit()
	try:
		param = '{"thread_id":"","action":4,"content":"%s","receiver_user_id":"%s","target_type":3,"user_id":188535207,"access_token":"7133217554889327475"}' % (text, uid)
		plant = 'poco_%s_app' % param
		m1 = md5.new()
		m1.update(plant)   
		m5 = m1.hexdigest()
		sign_code = m5[5:5+19]
		ctime = int(round(time.time() * 1000))
		req = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":%d,"param":%s,"sign_code":"%s"}' % (ctime, param, sign_code)
		data = {'host_port':'http://my.poco.cn', 'req':req}
		response = requests.post(url, cookies=cookie, data=data)
		resultJson = json.loads(response.text)
		if resultJson['code'] == 10000:
			message = resultJson['message'].encode('utf8')
			print rid, uid, message
		else:
			print rid, uid, response.text
		time.sleep(180)	
	except Exception, e:
		print e.message

cur.close()
conn.close()
