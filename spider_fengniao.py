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
		response = requests.get(url, cookies=cookie)
	except:
		return ''
	else:
		return response.content

def analyzeHtml(url, p):
	#p = r'(Email|qq|手机) : </span>(.*?)</div>'
	html = getHtml(url)
	pattern = re.compile(p)
	return pattern.findall(html)

def run(id, current_crawl_deep):
	global cur,conn,regionMap
	#global current_crawl_deep
	current_crawl_deep += 1
	#解析Email qq 手机
	#id = 324379
	#id = 10278436
	#result = analyzeHtml(html, r'QQ  ： (\d+)')
	result = analyzeHtml("https://my.fengniao.com/info.php?userid=%s" % id, r'<p>昵称 ： (.+?)</p>|<p>省份 ： (.+?)</p>|<p>微博 ： (.+?)</p>|<p>QQ  ： (.+)</p>')
	#print result[1][1]
	#exit()
	if result != []:
		nickname = result[0][0]
		province = result[1][1]
		weibo = result[2][2]
		qq = result[3][3]
		email = qq + '@qq.com'
		if qq == '暂无':
			qq = ''
			email = ''
			#没有QQ时分析相册、动态来决定是否为价值用户
			result = analyzeHtml("https://my.fengniao.com/album.php?userid=%s" % id, r'共<font class="num">(\d+)</font>个相册')
			if result[0] == '0':
				result = analyzeHtml("https://my.fengniao.com/index.php?userid=%s" % id, r'<div class="noInfo">暂时没有动态</div>')
				if result != []:
					return
		try:
			if province == '暂无':
				province = ''
			else:
				province = regionMap[province]
			if weibo == '暂无':
				weibo = ''
			sql = "insert into fengniao_log (user_id,email,qq,nickname,province,weibo) values('%s','%s','%s','%s','%s','%s')" % (id, email, qq, nickname, province, weibo)
			cur.execute(sql)
			conn.commit()
			print sql
		except Exception, e:
			print e.message


	if current_crawl_deep > 6:
		return


	#解析好友
	p = 1
	while True:
		url = "https://my.fengniao.com/friend.php?page=%d&userid=%s" % (p, id)
		id_list = analyzeHtml(url, r'<a href="javascript:void \(0\)" class="btn letterBtn" userId="(\d+)" userName=".*?" >私信</a>')
		for id in id_list:
			run(id, current_crawl_deep)
		next_page = analyzeHtml(url, '下页')
		if next_page == []:
			break;
		p += 1



cookie = {}
raw_cookies = 'p_ck=5MOD7/L3j7QuMzQyODgwLjE1MTc3NTI1OTI%3D; lv=1517752592; vn=1; bbuserid=10796194; bbpassword=adf234d78a156ef66ea02b63ad3e00b2; bbusername=sun417; Adshow=5; PHPSESSID=5cqk208is870c3gm2aat511d82; Hm_lvt_916ddc034db3aa7261c5d56a3001e7c5=1517750378,1518396757; Hm_lpvt_916ddc034db3aa7261c5d56a3001e7c5=1518448232'
for line in raw_cookies.split(';'):
	key,value = line.split("=", 1)
	cookie[key] = value

regionMap = {"北京" : "Beijing","上海" : "Shanghai","天津" : "Tianjin","重庆" : "Chongqing","福建" : "Fujian","辽宁" : "Liaoning","吉林" : "Jilin","河北" : "Hebei","海南" : "Hainan","陕西" : "Shaanxi","山西" : "Shanxi","甘肃" : "Gansu","宁夏" : "Ningxia","新疆" : "Xinjiang","西藏" : "Tibet","青海" : "Qinghai","四川" : "Sichuan","云南" : "Yunnan","贵州" : "Guizhou","湖南" : "Huonan","湖北" : "Huobei","河南" : "Henan","山东" : "Shandong","安徽" : "Anhui","江苏" : "Jiangsu","浙江" : "Zhejiang","台湾" : "Taiwan","香港" : "Hong Kong","澳门" : "Macau","广东" : "Guangdong","广西" : "Guangxi","江西" : "Jiangxi","黑龙江" : "Heilongjiang","内蒙古" : "Inner Mongolia","其他" : "Other","省/直辖市" : "Other"}
seed_id = '156286'	#种子url
conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

run(seed_id, 0)

cur.close()
conn.close()
