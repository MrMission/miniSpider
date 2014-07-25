#encoding=utf-8
import requests
from redis import Redis
import sys

class Crawler:
    def __init__(self, encode='utf-8', site=''):
        # 下载之前，初始化redis
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.encode = encode

    def crawl(self):
        # 遍历url_list，进行爬取，爬取的结果放在crawl_list
        url = self.r_server.rpop('url_list')
        while url:
            content = self._get_content(url)
            self.r_server.rpush('crawl_list', content)
            url = self.r_server.rpop('url_list')

    def _get_content(self, url):
        while 1:
            r = ''
            try:
                r = requests.get(url)
                print r
                r.encoding = self.encode
            except:
                s = sys.exc_info()
                print url
                print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            if r != '':
                break
        return r.text

if __name__ == "__main__":
    c = Crawler()
    c.crawl()

