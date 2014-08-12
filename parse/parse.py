from bs4 import BeautifulSoup
from redis import Redis
from time import sleep
import string
import json
import sys
from imp import reload
reload(sys)

class Parser():
    # 即从配置文件中读取东西，存入control中
    def configure(self):
        file = open('/home/Administrator/minispider/parse/spider.xml', 'r')
        content_list = file.readlines()
        content = ''.join(content_list)
        soup = BeautifulSoup(content)
        tags = soup.find_all('parser')
        for tag in tags:
            level = tag.find('level').text
            function = tag.find('function').text
            self.control[level] = function

    # 设置好redis，前缀，名字，以及得到配置文件
    def __init__(self, prefix, name, site=''):
        self.r_server = Redis()
        self.prefix = prefix
        self.name = name
        self.control = {}
        self.configure()
        print("初始化配置...")
        print(self.control)

    def parse(self):
        while True:
            try:
                dic = json.loads(self.r_server.blpop('crawl_list')[1].decode())
                if str(dic['level']) in self.control:
                    func = eval("self." + self.control[str(dic['level'])])
                    func(dic)
                    pass
            except:
                # 打印错误信息
                s = sys.exc_info()
                print('Error %s happened in line %d in %s' % (s[1], s[2].tb_lineno, s[0]))
                # 出错要把该信息放到error_list,且要重新放回到crawl_list
                self.r_server.rpush('error_list', json.dumps(dic))
                #self.r_server.rpush('crawl_list', json.dumps(dic))
            finally:
                # 再从crawl_list中取字典
                encode_dic = self.r_server.lpop('crawl_list')
    def getFirst(self, dic):
        print('getFirst')
        pass

    def getSecond(self, dic):
        print('getSecond')
        pass

    def getThird(self, dic):
        print('getThird')
        pass

    def getThird2(self, dic):
        pass

    def getWord(self, dic):
        print('getWord')
        pass

    def isEmpty(self):
        if self.r_server.llen('crawl_list') == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        name = sys.argv[1]
    else:
        name = 'res'
    p = Parser('http://detail.zol.com.cn', name)
    p.parse()
