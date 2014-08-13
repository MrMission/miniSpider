from redis import Redis
from bs4 import BeautifulSoup
import json

r_server = Redis()
# 那么要去解析下配置文件，把seed放进去
file = open('parse/spider.xml', 'r')
content = ''.join(file.readlines())
soup = BeautifulSoup(content, 'xml')
tags = soup.find_all('seed')
for tag in tags:
    url = tag.find('url').text
    encode = tag.find('encode').text
    level = 1
    dic = {'url': url, 'encode': encode, 'level': level}
    r_server.rpush('url_list', json.dumps(dic))
    print(url, encode, level)

