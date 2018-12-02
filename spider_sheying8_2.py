#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
from lxml import html
import traceback
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
	personList = analyzeHtml(html, r'<a href="http://([^>]+?).sheying8.com/" target="_blank">(.+?)</a>')
	for personId, personName in personList:
		try:
			if personId in uid_list:
				#print personId, '已经处理'
				continue
			uid_list.append(personId)
			personName = personName.decode('gbk').encode('utf8')
			#print spaceId,spaceName,personId,personName
			#exit()
			url = "http://%s.sheying8.com/Contact.asp" % personId
			print url
			html = getHtml(url)
			city = ""
			personName = getValue(analyzeHtml(html, r'</span> (.*?) <b class="caret"></b>')).decode('gbk').encode('utf8')
			studio = getValue(analyzeHtml(html, r'<input.*?value="(.*?)">')).decode('gbk').encode('utf8')
			mobile1 = getValue(analyzeHtml(html, r'Mob : (\d*?)\s+'))
			telphone1 = getValue(analyzeHtml(html, r'Tel : (\d*?)\s+'))
			qq = getValue(analyzeHtml(html, r'QQ : (\d*?)\s+'))
			email = getValue(analyzeHtml(html, r'<SPAN>E-mail：</SPAN>(.+?)</P>'.encode('gbk')))
			address = getValue(analyzeHtml(html, r'<SPAN>地址：</SPAN>(.*?)</P>'.encode('gbk')))
			mobile2 = getValue(analyzeHtml(html, r'<SPAN class=tel_address_tel_word>手机热线：</SPAN><SPAN class=tel_address_tel_tag>(\d*?)\s*</SPAN>'.encode('gbk')))
			telphone2 = getValue(analyzeHtml(html, r'<P class=not_open>座机请拨打：<SPAN>(\d*?)\s*</SPAN></P>'.encode('gbk')))
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
				print personId + " 已插入"
			print '=' * 100
		except Exception, e:
			print "Exception"
			print e
			msg = traceback.format_exc()
			print msg
			print '=' * 100
			pass

	print '*' * 20 + pageUrl + '*' * 20

def run():
	global cur,conn
	result = analyzeUrl("http://www.sheying8.com/photolist/", r'<a title="(.+)" href="http://www.sheying8.com/photolist/(.+)/" class="list-group-item nav-list-item">')
	for spaceName,spaceId in result:
		spaceName = spaceName.decode('gbk').encode('utf8')
		spaceUrl = "http://www.sheying8.com/photolist/%s/" % spaceId
		html = getHtml(spaceUrl)
		pages = analyzeHtml(html, r'共(\d+)页'.encode('gbk'))[0]
		for page in range(1, int(pages) + 1):
			url = spaceUrl + str(page) + '.shtml'
			getPerson(url, spaceId, spaceName)


conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()
uid_list = []

run()

cur.close()
conn.close()
