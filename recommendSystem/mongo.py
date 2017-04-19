'''
    码猿 推荐系统
'''
from pymongo import MongoClient
import re
conn = MongoClient(host="192.168.88.88", port=27017)
db = conn.CSDN
collect = db.pageHistory
sessionId_set = {}
for i in collect.find():
    try:
        if (re.findall('/libraryList/,*?', i['PageUri'])):
            if(i['SessionId'] not in sessionId_set):
                sessionId_set[i['SessionId']]=[i['PageUri']]
            else:
                if('.js' in i['PageUri'] or '.css' in i['PageUri']):
                    continue
                sessionId_set[i['SessionId']].append(i['PageUri'])
    except:
        continue


for i in sessionId_set.items():
    print(i)