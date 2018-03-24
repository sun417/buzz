#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
import time
import md5
import json
import random
from lxml import html
from var_dump import var_dump

#print random.randint(1,5)
#exit()

offset = sys.argv[1]
limit = sys.argv[2]

cookie = {}
raw_cookies = 'ip_ck=5MOD7/L3j7QuMzQyODgwLjE1MTc3NTI1OTI%3D; lv=1517752592; vn=1; PHPSESSID=5cqk208is870c3gm2aat511d82; Adshow=4; loginRefer=http%3A%2F%2Fmy.fengniao.com%2F; bbuserid=10803486; bbpassword=40fa28fae8e4f527130982b9b8b02dd3; bbusername=%E6%95%B0%E7%A0%81%E4%B8%96%E7%95%8C%E5%BE%90%E6%95%8F; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1517750378,1518396757; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1519140913'
for line in raw_cookies.split(';'):
	key,value = line.split("=", 1)
	cookie[key] = value

text = '老师您好，我是《数码世界》杂志摄影栏目的徐敏，为了为广大摄影爱好者搭建一个最具专业的摄影创作交流平台，现特开展“数码摄影2018年优秀作品评选”的春季赛评选活动。欢迎各位老师踊跃参与，详情请加微信15810683299，了解详情！'
chinese_space = '！'
url = 'https://my.fengniao.com/ajax/ajaxMessage.php'

conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
cur = conn.cursor()

result = cur.execute("select id,user_id,nickname from fengniao_log order by id limit %s, %s" % (offset, limit))
rows = cur.fetchmany(result)
old_r = -1
error_count = 0
for row in rows:
	rid,uid,nickname = row
	#rid,uid,nickname = (1,10803486,'sun417')
	#print rid,uid,nickname
	#exit()
	try:
		while True:
			r = random.randint(0,2)
			if r != old_r:
				break
		print r, old_r
		data = {'f_userid':uid,'nickname':nickname,'invite_content':text + chinese_space * r,'action':'sendMessage'}
		old_r = r
		response = requests.post(url, cookies=cookie, data=data)
		resultJson = json.loads(response.text)
		#print resultJson
		#exit()
		if resultJson['code'] == 1:
			#print response.text.encode('utf8')
			msg = resultJson['msg'].encode('utf8')
			print rid, uid, nickname, msg
			error_count = 0
		else:
			print rid, uid, nickname, response.text
			error_count = error_count + 1
			if error_count >= 10:
				exit()
		time.sleep(300)	
	except Exception, e:
		print e.message

cur.close()
conn.close()
