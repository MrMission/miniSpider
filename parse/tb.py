from bs4 import BeautifulSoup
import sys
import json
sys.path.append('.')
print(sys.path)
from parse import Parser


class taobao(Parser):
    # dic中有url、content、level，level没用，url来确保是哪一条，content是最重要的
    def getFirst(self, dic):
        try: 
            content = dic['content']
            
            soup = BeautifulSoup(content)
            jiadian = soup.find(class_="market-cat J_TBMarketCat tm7")
            lists = jiadian.find_all('li')

            del dic['content']
            dic['level'] = 2

            for list in lists:
                first = list.find('h5').text
                dic['first'] = first
                print(first)

                sublist = list.find(class_='sublist')
                tags = sublist.find_all('a')
                for tag in tags:
                    #print(tag.text)
                    dic['second'] = tag.text
                    dic['url'] = tag['href'] + '&json=on'
                    self.push(dic, 'url')
        except:
            s = sys.exc_info()
            print('Error %s happened in line %d in %s' % (s[1], s[2].tb_lineno, s[0]))

    def getSecond(self, dic):
        try:
            content = dic['content']

            en_dic = json.loads(content)
            propertyList = en_dic['propertyList']

            llist = []
            for property in propertyList[2: ]:
                name = property['name']
                subList = property['propertyList']
                t_list = []
                for sub_pro in subList:
                    t_list.append(sub_pro['name'])
                    #print(sub_pro['name'], end=',')
                #print()
                llist.append(name + ':' + ' '.join(t_list))

            dic['result'] = llist
            del dic['content']
            print(dic['first']) # for test
            self.push(dic, 'result')

        except:
            s = sys.exc_info()
            print('Error %s happened in line %d in %s' % (s[1], s[2].tb_lineno, s[0]))
            
        
if __name__ == '__main__':
    tb = taobao()
    tb.parse()
