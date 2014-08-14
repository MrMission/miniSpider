from redis import Redis
from time import sleep
import requests
import json
import sys
from time import sleep

class Crawler:
    # 全局变量来设定
    count = 0
    def __init__(self):
        # 初始化redis
        self.r_server = Redis()

    def pullCrawlRequest(self):
        return json.loads(self.r_server.blpop('url_list')[1].decode())
        '''
        while True:
            if not self.r_server.lpop('url_list'):
                return json.loads(self.r_server.lpop('url_list').decode())
            else:
                sleep(5)
        '''

    def pushParserRequest(self, dic):
        self.r_server.rpush('crawl_list', json.dumps(dic))

    def crawl(self):
        while True:
            # 从redis中取出要爬的url等信息
            dic = self.pullCrawlRequest()

            # 爬下来，然后放到redis中
            content = self._get_content(dic['url'], dic['encode'])
            del dic['url']
            dic['content'] = content
            self.pushParserRequest(dic)
            
            # 打印count
            self.__class__.count += 1
            print(self.__class__.count)

    def isEmpty(self):
        if self.r_server.llen('url_list') == 0:
            return True
        else:
            return False

    def _get_content(self, url, encode, method='GET', params=None):
        while True:
            try:
                if method == 'GET':
                    r = requests.get(url)
                else:
                    r = requests.post(url, data=params)
                r.encoding = encode
                return r.text
            except:
                s = sys.exc_info()
                print(url)
                print('Error %s happened in line %d' % (s[1], s[2].tb_lineno))
                sleep(5)

if __name__ == "__main__":
    c = Crawler()
    c.crawl()

