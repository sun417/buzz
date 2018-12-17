#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
from lxml import html
reload(sys)
sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()

def getHtml(url):
	global cookie
	try:
		response = requests.get(url)
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

def getPerson(pageUrl,spaceId, spaceName):
	#pageUrl = 'http://www.sheying8.com/spacelist/sheyingshi/20.shtml'
	html = getHtml(pageUrl)
	personList = analyzeHtml(html, r'<div class="padder-v text-person-list"><div>([^>]+?)</div><div><a href="http://(.+?).sheying8.com" target="_blank"  title="(.+?)" class="text-ellipsis">(.*?)</a></div>')
	for city, personId, studio, personName in personList:
		try:
			#print city,personId,studio,personName
			#exit()
			city = city.decode('gb2312').encode('utf8')
			studio = studio.decode('gb2312').encode('utf8')
			personName = personName.decode('gb2312').encode('utf8')
			#print spaceId,spaceName,city,personId,studio,personName
			#exit()
			url = "http://%s.sheying8.com/Contact.asp" % personId
			print url
			html = getHtml(url)
			mobile1 = getValue(analyzeHtml(html, r'Mob : (\d*?)\s+'))
			telphone1 = getValue(analyzeHtml(html, r'Tel : (\d*?)\s+'))
			qq = getValue(analyzeHtml(html, r'QQ : (\d*?)\s+'))
			email = getValue(analyzeHtml(html, r'<SPAN>E-mail：</SPAN>(.+?)</P>'.encode('gb2312')))
			address = getValue(analyzeHtml(html, r'<SPAN>地址：</SPAN>(.*?)</P>'.encode('gb2312')))
			mobile2 = getValue(analyzeHtml(html, r'<SPAN class=tel_address_tel_word>手机热线：</SPAN><SPAN class=tel_address_tel_tag>(\d*?)\s*</SPAN>'.encode('gb2312')))
			telphone2 = getValue(analyzeHtml(html, r'<P class=not_open>座机请拨打：<SPAN>(\d*?)\s*</SPAN></P>'.encode('gb2312')))
			sql = "select id from sheying8 where user_id='%s'" % personId
			count = cur.execute(sql)
			conn.commit()
			#count = cur.fetchmany(count)
			if count == 0:
				sql = "insert into sheying8 (user_id,name,type,studio,mobile1,telphone1,mobile2,telphone2,qq,email,city,address) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (personId,personName,spaceName,studio,mobile1,telphone1,mobile2,telphone2,qq,email,city,address)
				print sql
				cur.execute(sql)
				conn.commit()
			else:
				print personId + " inserted"
			print '=' * 100
		except Exception, e:
			print "Exception"
			print e
			print '=' * 100
			pass

	print '*' * 20 + pageUrl + '*' * 20

def run():
	global cur,conn
	result = analyzeUrl("http://www.sheying8.com/spacelist/", r'<a href="http://www.sheying8.com/spacelist/(.+)/" class="list-group-item nav-list-item" title="(.+)">')
	for spaceId, spaceName in result:
		spaceName = spaceName.decode('gb2312').encode('utf8')
		spaceUrl = "http://www.sheying8.com/spacelist/%s/" % spaceId
		html = getHtml(spaceUrl)
		pages = analyzeHtml(html, r'共(\d+)页'.encode('gb2312'))[0]
		for page in range(1, int(pages) + 1):
			url = spaceUrl + str(page) + '.shtml'
			getPerson(url, spaceId, spaceName)


conn = MySQLdb.connect(host='127.0.0.1', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

run()

cur.close()
conn.close()
