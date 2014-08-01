#encoding=utf-8

from bs4 import BeautifulSoup
from redis import Redis
from time import sleep
import string
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(object):
    def configure(self):
        file = open('spider.xml', 'r')
        content_list = file.readlines()
        content = ''.join(content_list)
        tags = soup.find_all('parser')
        for tag in tags:
            level = tag.find('level').text
            function = tag.find('function').text
            self.control[level] = function
    
    def __init__(self, prefix, name, site=''):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.prefix = prefix
        self.name = name
        self.control = {}
        self.configure()

    def parse(self):
        encode_dic = self.r_server.lpop('crawl_list')
        while encode_dic:
            try:
                # 从字典中得到内容以及level
                dic = json.loads(encode_dic)
                if self.control.has_key(dic['level']):
                    func = eval(self.control[dic['level']])
                    func()
                    pass
            except:
                # 打印错误信息
                s = sys.exc_info()
                print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
                # 出错要把该信息放到error_list,且要重新放回到crawl_list
                self.r_server.rpush('error_list', json.dumps(dic))
                self.r_server.rpush('crawl_list', json.dumps(dic))
            finally:
                # 再从crawl_list中取字典
                encode_dic = self.r_server.lpop('crawl_list')

    def isEmpty(self):
        if self.r_server.llen('crawl_list') == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    name = sys.argv[1]
    while True:
        p = Parser('http://detail.zol.com.cn', name)
        if p.isEmpty():
            sleep(5)
        p.parse()

