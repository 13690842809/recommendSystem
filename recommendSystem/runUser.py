from pymongo import MongoClient
import re
import time
import datetime
from userRecommend import *
conn = MongoClient(host="192.168.88.88", port=27017)
db = conn.CSDN
collect = db.my_user
while True:
    sysTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    recommend=userClass()
    for i in collect.find({},{"_id":0,"account":1,"recentLoginTime":1}):
        # print(i)#time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
        if(i['recentLoginTime']==''):
            # print(i['account'])
            continue
        #判断如果新登录用户 并且时间戳在100范围内就推荐
        if((time.mktime(time.strptime(sysTime,'%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime(i['recentLoginTime'],'%Y-%m-%d %H:%M:%S')))<=1):
            print('新登录用户:',i['account'])
            recommend.tfidf(i['account'])
            time.sleep(1)
        # print(time.mktime(time.strptime(sysTime,'%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime(i['recentLoginTime'],'%Y-%m-%d %H:%M:%S')))
    time.sleep(1)
    print('-----------')