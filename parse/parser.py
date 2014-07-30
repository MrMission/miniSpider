#encoding=utf-8
from bs4 import BeautifulSoup
from redis import Redis
import json
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(object):
    def __init__(self, prefix='', site=''):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.prefix = prefix

    def parse(self):
        #encode_dic = self.r_server.rpop('crawl_list')
        encode_dic = self.r_server.lpop('crawl_list')
        while encode_dic:
            try:
                # 从字典中得到内容以及level
                dic = json.loads(encode_dic)
                if dic['level'] == 1:
                    self.getFirst(dic)
                elif dic['level'] == 2:
                    self.getSecond(dic)
                elif dic['level'] == 3:
                    self.getThird(dic)
                elif dic['level'] == 4:
                    self.getWord(dic)
            except:
                # 打印错误信息
                s = sys.exc_info()
                print dic['url'], dic['level']
                print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
                # 如果出错要把这个信息放到error_list中
                self.r_server.rpush('error_list', json.dumps(dic))
            finally:
                # 再从crawl_list中取字典
                encode_dic = self.r_server.rpop('crawl_list')



    def getFirst(self, dic):
        try:
            content = dic['content']
            content = content.decode()
            dic['level'] = 2
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            div = soup.find(class_='all-item manuSwitch')
            tags = div.find_all('a')
            del dic['content']
            for tag in tags:
                dic['url'] = self.prefix + tag['href']
                dic['first'] = tag.text
                print dic['url'], dic['first']
                encode_dic = json.dumps(dic)
                self.r_server.rpush('url_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)

    def getSecond(self, dic):
        content = dic['content'].decode()
        dic['level'] = 3
        # 解析内容，得到url存进url_list
        soup = BeautifulSoup(content)
        div = soup.find(class_='series-list clearfix')
        if div:
            subdiv = div.find(class_='all-brand-list')
            if not subdiv:
                subdiv = div
            tags = subdiv.find_all('a')
            print '----------------------------------------------'
            print dic['url']
            del dic['content']
            for tag in tags:
                dic['url'] = self.prefix + tag['href']
                dic['second'] = tag.text
                print dic['url'], dic['first'], dic['second']
                encode_dic = json.dumps(dic)
                self.r_server.rpush('url_list', encode_dic)

    def getThird(self, dic):
        content = dic['content'].decode()
        dic['level'] = 4
        # 解析内容，得到url存进url_list
        soup = BeautifulSoup(content)
        tag = soup.find(class_='nav')
        href = tag.find(class_='a')['href']
        print '----------------------------------------------Third'
        print dic['url']
        del dic['content']
        dic['url'] = href
        print dic['url']
        encode_dic = json.dumps(dic)
        self.r_server.rpush('url_list', encode_dic)

    def getWord(self, dic):
        pass


if __name__ == "__main__":
    p = Parser('http://detail.zol.com.cn')
    p.parse()

           
