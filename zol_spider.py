#encoding=utf-8

from bs4 import BeautifulSoup
from redis import Redis
from time import sleep
import string
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('/home/Administrator/minispider/parse')
from parse import Parser

class zol_Parser(Parser):
    def getFirst1(self, dic):
        try:
            content = dic['content']
            content = content.decode()
            dic['level'] = 2
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            div = soup.find(class_='brand-sel-box clearfix')
            tags = div.find_all('a')
            del dic['content']
            print "---------------------------------First"
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
            raise

    def getSecond1(self, dic):
        try:
            content = dic['content'].decode()
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            dic['level'] = 3
            div = soup.find(class_='series-list clearfix')
            print '-------------------------------------------Second1'
            print len(soup)
            print div
            if div:
                print "xixi"
                subdiv = div.find(class_='all-brand-list')
                if not subdiv:
                    subdiv = div
                tags = subdiv.find_all('a')
                print dic['url']
                del dic['content']
                for tag in tags:
                    dic['url'] = self.prefix + tag['href']
                    dic['second'] = tag.text
                    print dic['url'], dic['first'], dic['second']
                    encode_dic = json.dumps(dic)
                    self.r_server.rpush('url_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            raise

    def getThird2(self, dic):
        try:
            content = dic['content'].decode()
            dic['level'] = 4
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            names = soup.find_all(class_='name')
            # 删除content，把配置这个页面的url得到
            del dic['content']
            print "-----------------------------Third"
            for name in names:
                dic['name'] = name.text
                print dic['url'], dic['first'], dic['second'], dic['name']
                # 把url存入url_list
                encode_dic = json.dumps(dic)
                self.r_server.rpush(self.name + '_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            raise

    def isEmpty(self):
        if self.r_server.llen('crawl_list') == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        print "Take Care!! the name is res..."
        name = 'res'
    while True:
        p = zol_Parser('http://detail.zol.com.cn', name)
        if p.isEmpty():
            sleep(5)
        p.parse()

