'''
    基于用户的协同过滤推荐系统(外链)
'''
from pymongo import MongoClient
import re
import numpy
import random
import pandas as pd
import datetime
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
class userClass:
    def __init__(self):
        conn = MongoClient(host="192.168.88.88", port=27017)
        db = conn.CSDN
        self.collect = db.pageHistory
        self.collect1 = db.ex_articleList
        self.collect2=db.userRecommend #打开用户推荐表
        self.recommend=db.recommend
        # self.testUser = '201406114223'  # 初始化测试用户
        self.recommendNum=30            #初始化推荐条数
        self.corpus=self.loadData()#
        # self.tfidf()


    def loadData(self):
        '''
            数据库查出用户纪录 构造 {用户1:['L1','L2'],用户2:['L2','L3']}
        '''
        username_set = {}
        for i in self.collect.find():
            try:
                if (re.findall('/externalLink/,*?', i['PageUri'])):
                    if (i['Username'] not in username_set):
                        username_set[i['Username']] = [i['PageUri']]
                    else:
                        if ('.js' in i['PageUri'] or '.css' in i['PageUri'] or 'get_libraryDetail' in i['PageUri']):
                            continue
                        username_set[i['Username']].append(i['PageUri'])
            except:
                continue

        '''
            1.提取标签号
            2.对应用户的数据去重
        '''
        goods = []  # 物品总
        self.users = {}  # 用户  物品（去重）
        for i in username_set:
            if (i == '未登录用户'):
                continue
            oneUser = []
            for j in username_set[i]:
                if (len(re.findall('\/', j)) == 2):
                    oneUser.append(re.findall('\/externalLink\/(.+)', j)[0])
                # else:
                #     oneUser.append(re.findall('\/externalLink\/(.+)\/.*?', j)[0])
                self.users[i] = list(set(oneUser))
                goods = list(set(goods).union(set(oneUser)))
                # data=list(set(data).union(set(list(set([(re.sub('\/.*?\/.*?\/','',x)) for x in username_set[i] if(len(re.findall('\/',x))>2)])))))#生成所有物品 不重复
                # print(i,list(set([(re.sub('\/.*?\/.*?\/','',x)) for x in username_set[i] if(len(re.findall('\/',x))>2)])))
        # print('用户:数据字典:', self.users)
        # print('物品列表(去重):', goods)
        len1 = len(goods)
        # print('物品数:', len1)

        '''
            计算tfidf前的数据准备 空格分割
        '''
        corpus = []
        self.username = []
        for i in self.users:
            str1 = ''
            self.username.append(i)
            for j in self.users[i]:
                str1 = str1 + j + ' '
            str1 = str1[:-1]
            corpus.append(str1)

        return corpus

    def tfidf(self,user):
        '''
            开始计算tfidf
        '''
        self.testUser = user
        if(user not in self.users):
            print('新用户 无轨迹:',user)
            self.newUserRecommend()
            return
        vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
        tfidf=transformer.fit_transform(vectorizer.fit_transform(self.corpus))
        SimMatrix = (tfidf * tfidf.T).A
        # print('参与推荐的用户:',self.testUser) #测试用户
        bin1=pd.DataFrame(data=SimMatrix,columns=self.username,index=self.username)#将用户相似度矩阵转换成dataframe
        binsort=bin1.sort_values(by=self.testUser) #按照测试用户排序
        bindrop=binsort[self.testUser].drop(self.testUser)#选择测试用户对应的相似度数据
        get_lastTwo=bindrop.tail(2).index #获取相似度最高的用户名
        one=list(set(self.users[get_lastTwo[1]]).intersection(set(self.users[self.testUser])))#两个用户之间做交集 推荐别人有的而我没有的
        two=list(set(self.users[get_lastTwo[0]]).intersection(set(self.users[self.testUser])))#两个用户之间做交集 推荐别人有的而我没有的
        # print('用户1喜欢的而你没选过的标签',one)
        # print('用户2喜欢的而你没选过的标签',two)

        common=list(set(one).union(set(two))) #并集 全集
        # common=list(set(one).intersection(set(two)))   #交集 共同拥有部分

        # print('共同的标签:',common)
        self.common=common
        if(self.common==[]):
            self.newUserRecommend()
        else:
            self.recommendData()

    def recommendData(self):
        # test = ['WoyLVXwZ', 'zSJRE3b8', 'RLV4K8pj', 'nDh7iLlE', 'LeoMgzIb', 'lGaEujN6', 'mrukFOw2', 'cJvq2xrm', ]
        eachTagNum = round(self.recommendNum / len(self.common))
        # print('每个标签推荐条数:',eachTagNum)
        data = []
        for tag in self.common:
            randomNum=self.collect1.find({"libraryCode": tag}).count()
            for i in self.collect1.find({"libraryCode": tag},{"_id": 0, "articleTitle": 1, "articleUrl": 1, "libraryName": 1}).limit(eachTagNum).skip(random.randint(1,randomNum)):  # 多值查询并筛选字段
                print(i)
                data.append(i)
            # print('---')
        print(len(data))
        self.collect2.insert({'userName':self.testUser,'recommendList':data,'nowTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    def newUserRecommend(self):
        '''
            新用户无纪录就从recommend中随机拿一条
        '''
        collectCount=self.recommend.find().count()
        print('条数:',collectCount)
        oneData=self.recommend.find({},{"_id":0}).limit(1).skip(random.randint(1,collectCount-1))
        for i in oneData:
            dictTemp=i
            dictTemp['userName'] = self.testUser
            self.collect2.insert(dictTemp)




# aa=userClass()
# aa.tfidf('avglp')



