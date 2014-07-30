#encoding=utf-8
from redis import Redis
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class storge:
    def __init__(self):
        self.r_server = Redis(host = 'localhost', port = 6379, db = 0)

    def store(self):
        f = open('/home/Administrator/miniSpider/data/computer.txt', 'w')
        for item in self.r_server.lrange('result_list', 0, -1):
            result = []
            dic = json.loads(item)
            result.append(dic['first'])
            result.append(dic['second'])
            result += dic['result']
            print result
            f.write(','.join(result) + '\n')
        f.close()

    def store_keyword(self):
        f = open('/home/Administrator/miniSpider/data/keyword.txt', 'w')
        for item in self.r_server.lrange('url_list', 0, -1):
            dic = json.loads(item)
            f.write(dic['first'] + ',' +  dic['second'] + '\n')
        f.close()

if __name__ == '__main__':
    s = storge()
    #s.store_keyword()
    s.store()
    
        
