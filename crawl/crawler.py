#encoding=utf-8
import requests
from redis import Redis
import json
import sys

class Crawler:
    count = 0
    def __init__(self, encode='utf-8', site=''):
        # 下载之前，初始化redis
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        if site != '':
            level = 1
            dic = {'url': site, 'level': level}
            encode_dic = json.dumps(dic)
            self.r_server.rpush('url_list', encode_dic)
        self.encode = encode

    def crawl(self):
        # 遍历url_list，进行爬取，爬取的结果放在crawl_list
        encode_dic = self.r_server.rpop('url_list')
        while encode_dic:
            # 打印count
            self.__class__.count += 1
            print self.__class__.count
            # 从字典中得到url以及内容
            dic = json.loads(encode_dic)
            url = dic['url']
            # 根据url下载相应的内容,存进去也是json
            content = self._get_content(url)
            dic['content'] = content
            encode_dic = json.dumps(dic)
            self.r_server.rpush('crawl_list', encode_dic)
            # 再从url_list中取字典
            encode_dic = self.r_server.rpop('url_list')

    def _get_content(self, url):
        while 1:
            r = ''
            try:
                r = requests.get(url)
                r.encoding = self.encode
            except:
                s = sys.exc_info()
                print url
                print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            if r != '':
                break
        return r.text

if __name__ == "__main__":
    #c = Crawler('gb2312', 'http://detail.zol.com.cn/notebook_index/subcate16_list_1.html')
    c = Crawler('gb2312')
    c.crawl()

