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
print sys.argv
offset = sys.argv[1]
limit = sys.argv[2]

cookie = {}
raw_cookies = 'visitor_flag=1512054951; visitor_r=; cmt_hash=1874997032; _topbar_introduction=1; g_session_id=d2efc69d914d4ff291f4e840b2f428e8; member_id=188504872; fav_userid=188504872; remember_userid=188504872; nickname=%CA%FD%C2%EB%CA%C0%BD%E7; fav_username=%CA%FD%C2%EB%CA%C0%BD%E7; activity_level=new; pass_hash=d2bc2f8d09990ebe87c809684fd78c66; session_ip=111.194.46.204; poco_user_msg=%7B%22user_id%22%3A188535207%2C%22expire_time%22%3A1527606405%2C%22access_token%22%3A%221249782998515021968%22%2C%22refresh_token%22%3A%225135779027375894790%22%2C%22nickname%22%3A%22%E6%95%B0%E7%A0%81%E4%B8%96%E7%95%8C%22%2C%22mobile%22%3A%22%22%2C%22email%22%3A%22%22%2C%22avatar%22%3A%22%2F%2Fimg1001.pocoimg.cn%2Fimage%2Fpoco%2Favatar%2F11%2F18853%2F188535207_1521819293_84666.jpg%22%2C%22area_code%22%3A%22%22%2C%22no_password%22%3Afalse%2C%22is_check%22%3A1%7D; Hm_lvt_5f160b35156601be1a20b4e58e497ecc=1523455657,1525014389; Hm_lpvt_5f160b35156601be1a20b4e58e497ecc=1525014749'
for line in raw_cookies.split(';'):
    key,value = line.split("=", 1)
    cookie[key] = value

text = '您好！我是《数碼世界》杂志摄影专栏徐敏，１５８１０６８３２９９同微信，欢迎您的摄影作品来我们杂志刊登发表、做专栏、专访！我们杂志正在回馈摄影人，邀请您参加由中国新時代摄影家协会 、《数碼世界》杂志社主办的首届“著名摄影师”暨“优秀摄影师”评选！'
url = 'http://web-api.poco.cn/v1_1/message/create_notify'

conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
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
		#param = '{"thread_id":"","action":4,"content":"%s","receiver_user_id":"%s","target_type":3,"user_id":188535207,"access_token":"2811521866772316641"}' % (text, uid)
		param = '{"thread_id":"","action":4,"content":"%s","receiver_user_id":"%s","target_type":3,"user_id":200827558,"access_token":"3764358321918930909"}' % (text, uid)
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
			message = resultJson['message'].encode('utf8')
			print rid, uid, message
		time.sleep(180)	
	except Exception, e:
		print e.message

cur.close()
conn.close()
