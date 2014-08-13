import requests
import re
from bs4 import BeautifulSoup

url = 'http://list.jd.com/list.html?cat=737,794,798'
r = requests.get(url)
content = r.text

soup = BeautifulSoup(content)
item = soup.find(class_='item current')
name = item.find('h3')
print(name.text)
tags = item.find_all('a')
file_name = ''.join(name.text.split(' '))
f = open(file_name + '.txt', 'w')
for tag in tags:
    try:
        print(tag['href'] + tag.text)

        url = tag['href']
        r = requests.get(url)
        content = r.text

        soup = BeautifulSoup(content)

        items = soup.find_all(class_=re.compile("prop-attrs"))
        res_list = []
        for item in items[1: -1]:
            c1 = item.find(class_='a-key')
            lis = item.find_all('li')
            c2_list = []
            for li in lis:
                c2_list.append(li.text)
            #print(c1.text + ' '.join(c2_list))
            res_list.append(c1.text + ' '.join(c2_list))
        f.write(','.join(res_list) + '\n')
    except:
        print(url)
f.close()

