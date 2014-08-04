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
            raise

    def getSecond2(self, dic):
        try:
            content = dic['content']
            content = content.decode()
            soup = BeautifulSoup(content)
            # 解析内容，得到下一页的url并存进url_list
            del dic['content']
            next_tag = soup.find(class_='next')
            if next_tag:
                dic['url'] = self.prefix + next_tag['href']
                encode_dic = json.dumps(dic)
                self.r_server.rpush('url_list', encode_dic)
            # 接下来解析该页面中是否有没有所属品牌的产品
            dic['level'] = 3
            print dic['url']
            tags = soup.find_all(class_='pro-intro')
            print "----------------------Second"
            for tag in tags:
                if not tag.find(text='所属：'):
                    dic['url'] = self.prefix + tag.find('a')['href']
                    dic['second'] = tag.find('a').text 
                    print dic['url'], dic['first'], dic['second']
                    encode_dic = json.dumps(dic)
                    self.r_server.rpush('url_list', encode_dic)
        except:
            # 打印错误信息
            s = sys.exc_info()
            print dic['url'], dic['level']
            print 'Error %s happened in line %d' % (s[1], s[2].tb_lineno)
            raise

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

    def getThird1(self, dic):
        try:
            content = dic['content'].decode()
            dic['level'] = 4
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            nav = soup.find(class_='nav')
            param = nav.find(text='参数')
            tag = param.parent
            # 删除content，把配置这个页面的url得到
            del dic['content']
            dic['url'] = self.prefix + tag['href']
            print "-----------------------------Third"
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
            print "-------------------------------Forth"
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

    def getWord1(self, dic):
        try:
            content = dic['content']
            content = content.decode()
            dic['level'] = 4
            # 解析内容，得到url存进url_list
            soup = BeautifulSoup(content)
            table = soup.find(class_="param_table")
            # 这里只是计数，没其他用途
            print dic['url'], dic['first'], dic['second']
            del dic['content']
            target = ['产品定位', 'CPU系列', 'CPU型号', '核心/线程数', '内存容量', '硬盘容量', '屏幕尺寸', '屏幕分辨率', '显卡类型', '显存容量']
            result = []
            result.append(dic['second'])
            for item in target:
                raw_c = table.find(text=item)
                if raw_c:
                    value = raw_c.find_next().text
                    result.append(value)
                else:
                    result.append('')
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
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        print "Take Care!! the name is res..."
        name = 'res'
    while True:
        p = Parser('http://detail.zol.com.cn/desktop_pc/', name)
        if p.isEmpty():
            sleep(5)
        p.parse()

