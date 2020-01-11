#-*-coding:utf-8-*-
import requests
import pymysql
import hashlib
import time
import json
import sys

def getData(param):
	plant = 'poco_%s_app' % param
	m5 = hashlib.md5(plant.encode(encoding='UTF-8')).hexdigest()
	sign_code = m5[5:5 + 19]
	ctime = int(round(time.time() * 1000))
	req = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":%d,"param":%s,"sign_code":"%s"}' % (ctime, param, sign_code)
	data = {'host_port': 'http://my.poco.cn', 'req': req}
	return data

def getJson(url, param):
	data = getData(param)
	response = requests.post(url, headers=headers, data=data)
	resultJson = json.loads(response.text)
	return resultJson

def run(uid, current_crawl_deep):
	global cur, conn, uidList
	if uid in uidList:
		return
	uidList.append(uid)
	sql = "select id from poco where user_id=%d" % uid
	count = cur.execute(sql)
	conn.commit()
	if count != 0:
		return
	current_crawl_deep += 1
	try:
		url = 'http://web-api.poco.cn/v1_1/space/get_user_works_list'
		param = '{"user_id": null, "visited_user_id": %d, "keyword": "", "year": 0, "works_type": 0, "length": 18, "start": 0}' % (uid)
		json = getJson(url, param)
		if json['code'] != 10000 :
			print("%d 的获取作品数量失败" % uid)
			return
		albumCount = json['data']['total'] #作品数量
		if albumCount == 0 :
			return
		url = 'http://web-api.poco.cn/v1_1/space/get_brief_user_info'
		param = '{"visited_user_id":%d,"user_id":null}' % uid
		json = getJson(url, param)
		data = json['data']
		fans_count = data['fans_count']
		follow_count = data['follower_count']
		user_name = data['nickname']
		user_name = user_name.replace("'", "")
		url = 'http://web-api.poco.cn/v1_1/space/get_user_profile'
		json = getJson(url, param)
		data = json['data']
		city = data['location_name']
		email = data['associate_email']
		qq = data['associate_qq']
		phone = data['associate_phone'][:30]
		gender = data['sex']
		age = data['age']
		introduce = data['description'][:255]
		equip = ''
		if data['equipment'].__contains__('camera'):
			equip = data['equipment']['camera']['brand_name'] + ' ' + data['equipment']['camera']['model_name']
		url = 'http://web-api.poco.cn/v1_1/integral/get_user_honor'
		json = getJson(url, param)
		data = json['data']
		score = data['level_point_info']['total_points']
		level = data['level_point_info']['level_name']
		if email == '' and qq != '':
			email = qq + '@qq.com'
		sql = "insert into poco (user_id, user_name, city, email, qq, phone, gender, age, equip, introduce, level, score, album_count, fans_count, follow_count) " \
		"value (%d,'%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s',%d,%d,%d,%d)" % (uid, user_name, city, email, qq, phone, gender,age,equip,introduce,level,score,albumCount,fans_count,follow_count)
		try:
			cur.execute(sql)
			conn.commit()
			print('%d - %s' % (uid, user_name))
			time.sleep(5)
		except Exception as e:
			print('%d - %s - %s' % (uid, user_name, e))
			pass

		if current_crawl_deep > 12:
			return


		#解析好友
		p = 0
		while True:
			url = 'http://web-api.poco.cn/v1_1/space/get_user_follow_list'
			param = '{"user_id":null,"visited_user_id":%d,"length":18,"start":%d}' % (uid, p * 18)
			json = getJson(url, param)
			data = json['data']
			for user in data['list'] :
				run(user['user_id'], current_crawl_deep)
			if not data['has_more'] :
				break
			p += 1
	except Exception as e:
		print('%d - %s' % (uid, e))
		pass

def getUidList():
	global cur, conn
	uidList = []
	sql = 'select distinct user_id from poco'
	cur.execute(sql)
	uidTuple = cur.fetchall()
	for uid in uidTuple:
		uidList.append(uid[0])
	return uidList


conn = None
cur = None
uidList = []
headers = {
	'Accept': '*/*',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'http://www.poco.cn',
	'Referer': 'http://www.poco.cn/',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

def main():
	global  conn, cur, uidList
	conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='123123', db='spider', charset='utf8')
	cur = conn.cursor()
	uidList = getUidList()
	seed_id = int(sys.argv[1])# 种子url
	run(seed_id, 0)
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()
