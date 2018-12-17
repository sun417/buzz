# -*- coding: UTF-8 -*-
import sys
import requests
import re
import MySQLdb
import time
from lxml import etree
#from var_dump import var_dump
reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://docs.amazonaws.cn/general/latest/gr/rande.html'
response = requests.get(url)
response.encoding='utf-8'
html = etree.HTML(response.content)
data = html.xpath('//*[@id="w108aab7d216b7"]/tr/td')
if len(data) == 0:
	exit()

#conn = MySQLdb.connect(host='10.59.216.87', port = 4293, user='root', passwd='Nb!9RT9y1x', db ='msp', charset='utf8')
#cur = conn.cursor()
#sql = 'delete from msp_aws_region'
#cur.execute(sql)
#conn.commit()
for i in range(0, len(data)):
	if i % 6 == 0:
		#print i,data[i][0].encode('utf8')
		regionName = data[i].text.encode('utf8')
		regionId = data[i+1].text.encode('utf8')
		print regionName,regionId
#		sql = "insert into msp_aws_region (regionName,regionId) values('%s','%s')" % (regionName,regionId)
#		try:
#			cur.execute(sql)
#			conn.commit()
#		except:
#			pass
#cur.close()
#conn.close()
