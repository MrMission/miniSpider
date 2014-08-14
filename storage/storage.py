from redis import Redis
import json
import sys
from time import sleep
from imp import reload
reload(sys)

class storge:
    def __init__(self, name):
        self.r_server = Redis()
        self.name = name

    def store(self):
        f = open('./data/' + self.name + '.txt', 'w')
        for item in self.r_server.lrange(self.name + '_list', 0, -1):
            result = []
            dic = json.loads(item.decode())
            result.append(dic['first'])
            result.append(dic['second'])
            if dic['result'] == []:
                continue
            result += dic['result']
            print(dic['result'])
            f.write(','.join(result) + '\n')
        f.close()

    def store_mengqi(self):
        f = open('./data/' + self.name + '.txt', 'w')
        for item in self.r_server.lrange(self.name + '_list', 0, -1):
            result = []
            dic = json.loads(item)
            result += dic['result']
            f.write(','.join(result) + '\n')
        f.close()

    def store_keyword(self):
        f = open('./data/' + self.name + '.txt', 'w')
        for item in self.r_server.lrange(self.name + '_list', 0, -1):
            dic = json.loads(item)
            f.write(dic['first'] + ',' +  dic['second'] + ',' + dic['result'][0] + '\n')
        f.close()

    def is_finish(self):
        if self.r_server.llen('url_list') == 0 and self.r_server.llen('crawl_list') == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    #name = 'netbook'
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        print("Take Care, you'd better to add file's name, now your file's name is result.")
        name = "result"
    s = storge(name)
    if s.is_finish():
        s.store()
        
