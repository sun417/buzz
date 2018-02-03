#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
from lxml import html

def getHtml(url):
	try:
		response = requests.get(url)
		response.encoding = 'gbk'
	except:
		return ''
	else:
		return response.content

def analyzeHtml(url, p):
	html = getHtml(url)
	print html
	exit()
	pattern = re.compile(p)
	return pattern.findall(html)

def getForum(fid):
	global uins
	result = analyzeHtml('http://bbs.photofans.cn/forum-%s-1.html' % fid, r'<span title="\xb9\xb2 (\d+) \xd2\xb3">')
	page = int(result[0])
	for i in range(1,page + 1):
		result = analyzeHtml('http://bbs.photofans.cn/forum-%s-%s.html' % (fid, i), r'home.php\?mod=space&amp;uid=(\d+)')
		for uin in result:
			if uin in uins:
				continue
			if len(uins) > 1000:
				del uins[0]
			uins.append(uin)
			r = analyzeHtml('http://bbs.photofans.cn/space-uid-%s.html' % uin, r'<li><em>QQ</em>(\d+)</li>')
			if len(r) == 0 or r == ['0']:
				continue
			sql = "insert into photofans_log (user_id,qq) values('%s','%s')" % (uin, r[0])
			try:
				cur.execute(sql)
				conn.commit()
			except:
				pass

			print sql
		


def run(start_url):
	global cur,conn
	result = analyzeHtml(start_url, r'http://bbs.photofans.cn/forum-(\d+)-1.html')
	fids = []
	for fid in result:
		if fid not in fids:
			fids.append(fid)
	
	for fid in fids:
		getForum(fid)
		




conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

uins = []

run('http://bbs.photofans.cn/forum.php')

cur.close()
conn.close()
