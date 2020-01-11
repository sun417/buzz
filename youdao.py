import getopt
import sys
import re
import urllib.request
import xml.etree.ElementTree as ET
#有道词典api接口
URL= 'http://fanyi.youdao.com/openapi.do?keyfrom=youdaoci&key=694691143&type=data&doctype=xml&version=1.1'
#从互联网获取请求信息
def response(words):
    query =  urllib.request.urlopen(URL + '&q=' + words)
#返回xml页面
    return query

def show_xml(resu):
#解析xml结果
    tree = ET.parse(resu)
    root = tree.getroot()
    loop(root)

#递归输出内容
def loop(root):
    for child in root:
        if child:
            loop(child)
        else:
            print(child.text)
    
def main():
    try:
      #从命令行接受要查询的单词
        options, args = getopt.getopt(sys.argv[1:],'h', ['help'])
    except getopt.GetoptError as e:
        pass
    #将输入的内容转换成小写
    match = re.findall(r'[\w.]+', " ".join(args).lower())
    #输入内容很多事用空格连接
    words = "_".join(match)
    resu = response(words)
    if not resu:
        return
    root = show_xml(resu)
    
if __name__=='__main__':
    main()