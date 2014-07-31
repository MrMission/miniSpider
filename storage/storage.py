#encoding=utf-8
from redis import Redis
import json
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')
class storge:
    def __init__(self, name):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)
        self.name = name

    def store(self):
        f = open('/home/Administrator/miniSpider/data/computer.txt', 'w')
        for item in self.r_server.lrange(self.name + '_list', 0, -1):
            result = []
            dic = json.loads(item)
            result.append(dic['first'])
            result.append(dic['second'])
            result += dic['result']
            print result
            f.write(','.join(result) + '\n')
        f.close()

    def store_keyword(self):
        f = open('/home/Administrator/miniSpider/data/' + self.name + '.txt', 'w')
        for item in self.r_server.lrange(self.name + '_list', 0, -1):
            dic = json.loads(item)
            f.write(dic['first'] + ',' +  dic['second'] + '\n')
        f.close()

    def is_finish(self):
        if self.r_server.llen('url_list') == 0 and self.r_server.llen('crawl_list') == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    #name = 'netbook'
    name = sys.argv[1]
    s = storge(name)
    is_save = False
    while True:
        if s.is_finish():
            s.store_keyword()
            is_save = True
        if is_save:
            break
        sleep(5)
        #s.store()
    
        
