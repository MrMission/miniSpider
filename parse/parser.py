#encoding=utf-8
from bs4 import BeautifulSoup
from redis import Redis
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(object):
    def __init__(self, prefix='', site=''):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.prefix = prefix

    def parse(self):
        encode_dic = self.r_server.rpop('crawl_list')
        while encode_dic:
            # 从字典中得到内容以及level
            dic = json.loads(encode_dic)
            if dic['level'] == 1:
                self.getFirst(dic)
            # 再从crawl_list中取字典
            encode_dic = self.r_server.rpop('crawl_list')

    def getFirst(self, dic):
        content = dic['content']
        content = content.decode()
        dic['level'] = 2
        # 解析内容，得到url存进url_list
        del dic['content']
        soup = BeautifulSoup(content)
        div = soup.find(class_='all-item manuSwitch')
        tags = div.find_all('a')
        for tag in tags:
            dic['url'] = self.prefix + tag['href']
            print dic['url']
            encode_dic = json.dumps(dic)
            self.r_server.rpush('url_list', encode_dic)

if __name__ == "__main__":
    p = Parser('http://detail.zol.com.cn')
    p.parse()

