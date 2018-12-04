#-*-coding:utf-8-*-
import sys
import requests
import time
import random
import re
import MySQLdb
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()

def getHtml(url):
	global cookie,headers
	try:
		response = requests.get(url)
		time.sleep(50)
		#print response.content
	except:
		return ''
	else:
		return response.content

def analyzeHtml(html, p):
	pattern = re.compile(p)
	return pattern.findall(html)

def analyzeUrl(url, p):
	html = getHtml(url)
	pattern = re.compile(p)
	return pattern.findall(html)

def getValue(result):
	if len(result) == 0:
		return ''
	else:
		return result[0]

def getPerson(spaceUrl, spaceId, name):
	#spaceUrl = 'http://my.nphoto.net/scdd_tb/'
	#spaceUrl = 'http://my.nphoto.net/qxss/'
	try:
		html = getHtml(spaceUrl)
		address = ','.join(analyzeHtml(html, r'<a href="http://my.nphoto.net/users/search\?country=.*?">(.+?)</a>'))
		lastLogin = '-'.join(analyzeHtml(html, r'最后登录：(\d{4})/(\d{2})/(\d{2})')[0])
		qq = analyzeHtml(html, r'alt="QQ"></td>\s+<td>(.+?)</td>')
		qq = qq[0] if len(qq) == 1 else ''
		email = analyzeHtml(html, r'alt="Email"></td>\s+<td>(.+?)<img src="http://static.nphoto.net/images/icon_at.gif" border="0">(.+?)</td>')
		email = '@'.join(email[0]) if len(email) == 1 else ''
		msn = analyzeHtml(html, r'alt="MSN"></td>\s+<td>(.+?)<img src="http://static.nphoto.net/images/icon_at.gif" border="0">(.+?)</td>')
		msn = '@'.join(msn[0]) if len(msn) == 1 else ''
		cameras = ','.join(analyzeHtml(html, r'<a href="http://dc.nphoto.net/cameras/.*?/">(.+?)</a>'))
		lenses = ','.join(analyzeHtml(html, r'<a href="http://dc.nphoto.net/lenses/.*?/">(.+?)</a>'))
		print spaceId,name,address,lastLogin,qq,email,msn,cameras,lenses
		sql = "select id from nphoto where user_id='%s'" % spaceId
		count = cur.execute(sql)
		conn.commit()
		if count == 0:
			sql = "insert into nphoto (user_id,name,address,lastlogin,qq,email,msn,cameras,lenses) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (spaceId,name,address,lastLogin,qq,email,msn,cameras,lenses)
			cur.execute(sql)
			conn.commit()
		else:
			print spaceId,"inserted"	
	except Exception, e:
		print  e
	print '=' * 100
	

	return

def run():
	global cur,conn
	for page in range(1,1569):
		url = 'http://blog.nphoto.net/blogs?t=31374&p=%d' % page
		#print url
		result = analyzeUrl(url, r'<a href="http://blog.nphoto.net/(.+?)/" title="查看.*?" target="_blank">(.+?)</a>')
		#print result
		#exit()
		for spaceId, name in result:
			spaceUrl = 'http://my.nphoto.net/%s/' % spaceId
			getPerson(spaceUrl, spaceId, name)
		print '*' * 100
		#exit()

cookie = {}
raw_cookies = 'Cookie:JSESSIONID=abcxIM_dFf4HHfx8BFLkw; lastvisit=1523376043436; last_ad_popup=0; last_hit_ad=0; uid=8a2b978a62837c7a01629617aad210b4; pwd=4f5f3c2adbcc8752f1e2e4b81ea188c4; sid=8a2b978a62837e890162b4fb961b063c; rm=1'
for line in raw_cookies.split(';'):
	key,value = line.split("=", 1)
	cookie[key] = value


conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider', charset='utf8')
cur = conn.cursor()

run()

cur.close()
conn.close()
