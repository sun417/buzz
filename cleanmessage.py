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

def getMessageList():
	try:
		get_message_list_url = 'http://web-api.poco.cn/v1_1/message/get_message_list'
		param = '{"action":4,"start":0,"length":20,"user_id":188535207,"access_token":"2811521866772316641"}'
		plant = 'poco_%s_app' % param
		m1 = md5.new()
		m1.update(plant)
		m5 = m1.hexdigest()
		sign_code = m5[5:5+19]
		ctime = int(round(time.time() * 1000))
		req = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":%d,"param":%s,"sign_code":"%s"}' % (ctime, param, sign_code)
		data = {'host_port':'http://my.poco.cn', 'req':req}
		response = requests.post(get_message_list_url, cookies=None, data=data)
	except Exception, e:
		print e.message
	else:
		resultJson = json.loads(response.text)
		return resultJson

def delMessage(thread_id):
	delete_thread_url = 'http://web-api.poco.cn/v1_1/message/delete_thread'
	param = '{"thread_id":"%s","user_id":188535207,"access_token":"2811521866772316641"}' % thread_id
	plant = 'poco_%s_app' % param
	m1 = md5.new()
	m1.update(plant)   
	m5 = m1.hexdigest()
	sign_code = m5[5:5+19]
	ctime = int(round(time.time() * 1000))
	req = '{"version":"1.1.0","app_name":"poco_photography_web","os_type":"weixin","is_enc":0,"env":"prod","ctime":%d,"param":%s,"sign_code":"%s"}' % (ctime, param, sign_code)
	data = {'host_port':'http://my.poco.cn', 'req':req}
	try:
		response = requests.post(delete_thread_url, cookies=None, data=data)
	except Exception, e:
		print e.message
	else:
		print response.text



if __name__ == '__main__':
	while True:
		messageList = getMessageList()
		if messageList['code'] != 10000:
			print 'get message list error'
			exit()
		for item in messageList['data']['list']:
			if item['last_send_user'] == '188535207' and item['last_content'].startswith(u'您好！我是《数码世界》杂志摄影专栏徐敏'):
				delMessage(item['thread_id'])
				time.sleep(15)
		if len(messageList['data']['list']) != 20:
			break;
