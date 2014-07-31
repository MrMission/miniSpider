#encoding=utf-8

from bs4 import BeautifulSoup
from redis import Redis
import json
import string
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(object):
    def __init__(self, prefix, name, site=''):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.prefix = prefix
        self.name = name

    def parse(self):
        #encode_dic = self.r_server.rpop('crawl_list')
        encode_dic = self.r_server.lpop('crawl_list')
        while encode_dic:
            try:
                # 从字典中得到内容以及level
                dic = json.loads(encode_dic)
                if dic['level'] == 1:
                    # Note 
                    #self.getFirst(dic)
                    self.getFirst1(dic)
                elif dic['level'] == 2:
                    pass
                    #self.getSecond(dic)
                    self.getSecond1(dic)
                elif dic['level'] == 3:
                    pass
                    #self.getThird(dic)
                elif dic['level'] == 4:
                    pass
                    #self.getWord(dic)
            except:
                # 打印错误信息
                s = sys.exc_info()
                print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
                # 如果出错要把这个信息放到error_list中,而且要重新返回
                self.r_server.rpush('error_list', json.dumps(dic))
                self.r_server.rpush('crawl_list', json.dumps(dic))
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
            raise

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

    def getSecond(self, dic):
        try:
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
                    self.r_server.rpush(self.name + '_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)

    def getThird(self, dic):
        try:
            content = dic['content'].decode()
            dic['level'] = 4
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            nav = soup.find(class_='nav')
            tag = nav.find('a')
            # 删除content，把配置这个页面的url得到
            del dic['content']
            dic['url'] = self.prefix + tag['href']
            print dic['url'], dic['first'], dic['second']
            # 把url存入url_list
            encode_dic = json.dumps(dic)
            self.r_server.rpush('url_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            raise

    def getWord(self, dic):
        try:
            content = dic['content'].decode()
            dic['level'] = 5
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            table = soup.find(id="seriesParamTableBox")
            # 这里只是计数，没其他用途
            print dic['url'], dic['first'], dic['second']
            del dic['content']
            target = ['型号', '产品定位', 'CPU系列', 'CPU型号', '核心/线程数', '内存容量', '硬盘容量', '屏幕尺寸', '屏幕分辨率', '显卡类型', '显存容量']
            temp_dic = {}
            num = int(table.find('table')['class'][1].split('_')[1])
            for item in target:
                c = ['' for i in range(num)]
                raw_c = table.find(text=item)
                if raw_c:
                    p = raw_c.findParents('tr')
                    c = p[0].find_all('td')
                temp_dic[item] = c
            for i in range(num):
                result = []
                for j in range(len(target)):
                    if temp_dic[target[j]][i] == '':
                        result.append('')
                    else:
                        result.append(temp_dic[target[j]][i].text)
                # 把result存入url_list
                dic['result'] = result
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
    name = sys.argv[1]
    while True:
        p = Parser('http://detail.zol.com.cn', name)
        if p.isEmpty():
            sleep(5)
        p.parse()

