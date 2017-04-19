# 推荐系统
##1.游客的推荐   
- 游客的推荐原理是从数据库中(10大类152小类,小类属于某大类)加载数据  
- 每一个大类所属的小类都统一起来归于此大类  
  构造成{'大类1':['数据1','数据2','数据n'], '大类2':['数据1','数据2','数据n']}  
 ####推荐的算法:  
 > 每个大类随机推荐10条数据 共100条  
 ####代码块
``` python
ii=0
classfication={}
for i in self.tenDict:
    classfication['classfication'+str(ii+1)]=[self.bigClass[ii],random.sample(self.tenDict[i], 10)]
    ii+=1
```
  
####游客推荐系统与后台交互原理:
> 从访问记录表(pageHistory)中实时查询总数(count),判断是否大于一个阀值(初始定为10条)  
记录表增加10条数据后便执行一次随机推荐100条数据,每个大类10条.
####代码块
``` python
baseCount = collect.find().count()
print('初始化条数',baseCount)
guest=guestClass()
while True:
    nowNum=collect.find().count()
    if((nowNum-baseCount)>10):
        guest.run()
        baseCount=nowNum
    time.sleep(1)
```
##2.用户登录后的推荐
###1).新注册用户(无用户轨迹随机推荐)
> 从游客推荐表中随机获取一次推荐作为新用户的推荐

###2).老用户(基于用户的协同过滤算法推荐)
- 先取出每个用户的行为记录.  
- 计算要推荐的用户与其他用户间的相似度,排序取出相似度最高的前两个. 
- 获取这两个用户共同所喜欢的小分类. 
- 基于这些小分类从数据库中分别随机平均的拿对应的数据. 
- 判断为哪个用户  
####代码块
``` python
eachTagNum = round(self.recommendNum / len(self.common))
# print('每个标签推荐条数:',eachTagNum)
data = []
for tag in self.common:
    randomNum=self.collect1.find({"libraryCode": tag}).count()
    # 多值查询并筛选字段
    for i in self.collect1.find({"libraryCode": tag},{"_id": 0, "articleTitle": 1,  
     "articleUrl": 1, "libraryName": 1}).limit(eachTagNum).skip(random.randint(1,randomNum)):  
        data.append(i)
```
####用户推荐系统与后台交互原理:
> 从用户信息表(my_user)中实时的检查每个用户的登录时间(recentLoginTime)  
计算当前时间与用户历史登录时间的时间戳只差,如果小于1则判断为用户已登录并执行推荐算法  
####代码块
``` python
sysTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for i in collect.find({},{"_id":0,"account":1,"recentLoginTime":1}):
    #判断如果新登录用户 并且时间戳在100范围内就推荐
    if((time.mktime(time.strptime(sysTime,'%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime(i['recentLoginTime'],'%Y-%m-%d %H:%M:%S')))<=1):
        print('新登录用户:',i['account'])
        recommend.tfidf(i['account'])#推荐算法调用
        time.sleep(1)
time.sleep(1)
```  

####此推荐系统分为两个python脚本,一直运行在后台,实时检查数据表实现数据推荐