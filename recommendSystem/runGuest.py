from pymongo import MongoClient
import re
import time
import datetime
from userRecommend import *
from guestRecommend import *
conn = MongoClient(host="192.168.88.88", port=27017)
db = conn.CSDN
collect = db.pageHistory
baseCount = collect.find().count()
print('初始化条数',baseCount)
guest=guestClass()
while True:
    nowNum=collect.find().count()
    print('---nowNum:',nowNum,'baseCount:',baseCount,nowNum-baseCount)
    if((nowNum-baseCount)>10):
        guest.run()
        baseCount=nowNum
    # print('-----')
    time.sleep(1)