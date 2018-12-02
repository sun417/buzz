#-*-coding:utf-8-*-
import sys
import requests
import re
import MySQLdb
from lxml import html

def getHtml(url):
	global cookie
	try:
		response = requests.get(url, cookies=cookie)
	except:
		return ''
	else:
		return response.content

def analyzeHtml(html, p):
	#p = r'(Email|qq|手机) : </span>(.*?)</div>'
	pattern = re.compile(p)
	return pattern.findall(html)

def run(id, current_crawl_deep):
	global cur,conn
	#global current_crawl_deep
	current_crawl_deep += 1
	#解析Email qq 手机
	url = "http://my.poco.cn/v2-mypoco_user_info-htx-user_id-%s.shtml" % id
	html =  getHtml(url)
	result = analyzeHtml(html, r'(Email|qq|\xca\xd6\xbb\xfa) : </span>(.*?)</div>')
	if result != []:
		email = ''
		qq = ''
		phone = ''
		for item in result:
			if item[0] == 'Email' and not item[1] in ['\xca\xd6\xbb\xfa', '\xba\xc3\xd3\xd1\xbf\xc9\xbc\xfb', '\xcb\xbd\xc3\xdc']:
				email = item[1]
			elif item[0] == 'qq' and not item[1] in ['\xca\xd6\xbb\xfa', '\xba\xc3\xd3\xd1\xbf\xc9\xbc\xfb', '\xcb\xbd\xc3\xdc']:
				qq = item[1]
			elif not item[1] in ['\xca\xd6\xbb\xfa', '\xba\xc3\xd3\xd1\xbf\xc9\xbc\xfb', '\xcb\xbd\xc3\xdc']:
				phone = item[1]
		if email != '' or qq != '' or phone != '':
			sql = "insert into spider_log (user_id,email,qq,phone) values('%s','%s','%s','%s')" % (id, email, qq, phone)
			try:
				cur.execute(sql)
				conn.commit()
			except:
				pass

			print sql

	if current_crawl_deep > 7:
		return


	#解析好友
	p = 1
	while True:
		url = "http://my.poco.cn/v2/mypoco_friends.htx&p=%d&user_id=%s&type=follow" % (p, id)
		html = getHtml(url)
		id_list = analyzeHtml(html, r'c_i64x64.*?id-(\d+)\.shtml')
		for id in id_list:
			run(id, current_crawl_deep)
		next_page = analyzeHtml(html, '下一页')
		if next_page == []:
			break;
		p += 1



cookie = {}
raw_cookies = 'ession_ip=111.194.47.40;session_id=d9d2d52790d5cae360ce6ca3c2d3a473;visitor_flag=1512054951;visitor_p=mypoco.css;visitor_r=;cmt_hash=1874997032;session_auth_hash=8cc78be16184b1f27fc1af4c5e06ae06;session_ip_location=101001001;_topbar_introduction=1;world_user_login=1;g_session_id=d2efc69d914d4ff291f4e840b2f428e8;member_id=188420364;fav_userid=188420364;remember_userid=188420364;nickname=%BE%C5%D4%C2;fav_username=%BE%C5%D4%C2;activity_level=new;pass_hash=00568afbe2cdb7828df6d20d3953433b;lastphoto_show_mode=list;visitor_b=mypoco.css;visitor_l=poco_tj.css;_current_time=1512139797.424'
for line in raw_cookies.split(';'):
    key,value = line.split("=", 1)
    cookie[key] = value

seed_id = '174391818'	#种子url
conn = MySQLdb.connect(host='localhost', port = 3306, user='root', passwd='123123', db ='spider')
cur = conn.cursor()

run(seed_id, 0)

cur.close()
conn.close()



#'http://my.poco.cn/v2-mypoco_friends-htx-user_id-36962703.shtml'
#seed_url = 'http://my.poco.cn/v2-mypoco_friends-htx-user_id-188420364.shtml'	#种子url
#current_crawl_deep = 0	#当前爬行深度
#html = getHtml(seed_url)
#id_list = analyzeId(html)
#print id_list
#http://my.poco.cn/v2-mypoco_friends-htx-user_id-178276054.shtml 好友列表
#http://my.poco.cn/v2-mypoco_user_info-htx-user_id-178276054.shtml 关于我

#(Email|qq|手机) : </span>(.*?)</div>
#c_i64x64.*?id-(\d+)\.shtml
#http://my.poco.cn/v2/mypoco_friends.htx&p=1&user_id=36962703&type=follow 翻页
#create table spider_log (id int unsigned not null auto_increment,user_id int not null unique,email varchar(255) not null default '', qq varchar(255) not null default '', phone varchar(255) not null default '',primary key (id));
