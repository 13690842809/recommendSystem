'''
    游客推荐系统
    随机推荐:10个大类的小类整合成十堆数据  每次运行从十堆数据中拿随机10条
'''
import random
from pymongo import MongoClient
import datetime

class guestClass:
    def __init__(self):
        conn = MongoClient(host='192.168.88.88', port=27017)
        self.db = conn.CSDN
        self.collect = self.db.recommend#推荐表 定时更新
        self.bigClass=['移动开发','云计算/大数据','编程语言','数据库','软件工程','前端开发','智能硬件','理论基础','操作系统','综合应用']
        self.step1()

    def step1(self):
        '''
            全部文章存入 全部小标签堆成10个大类
        '''
        collect2 = self.db.ex_articleList  # 文章
        self.dictBig = {'移动开发': ['Cocos2d-x', 'Android Wear', 'Weex', 'APK', 'Instagram', '微信小程序', 'Android', 'iOS', 'APP', 'Android Studio', 'React Native', 'Objective-C', 'Unity3D', 'Swift'],
                   '云计算/大数据': ['ECharts', 'HBase', 'SaaS', 'Scrapy', 'Docker', 'ZooKeeper', '数据分析', 'Apache Mesos','Apache Flume', 'MariaDB', 'HDFS', 'Apache Hive', 'OpenStack', 'Kafka', 'Yarn', 'NoSQL', 'Scala', '深度学习', 'Spark', '爬虫', 'Hadoop', '数据挖掘', '数据可视化', '云计算', '人工智能'],
                   '编程语言': ['函数式编程', 'JSON', 'Ruby ', '编程语言', '汇编语言', 'Oracle', 'ThinkPHP', 'C#', 'Java EE', 'R',  'Shell', 'SQL', 'Scala', '.NET', 'Go', 'C', '后端', 'Java', 'Python', 'PHP', 'C++'],
                   '数据库': ['SQLite', '数据库', 'MySQL', 'MongoDB', 'Redis'],
                   '软件工程': ['单元测试', 'Apache', 'MyBatis', '测试', 'Git', 'MVC', 'Spring Boot', 'OpenCV', 'MVP', '区块链', 'Spring', 'GitHub', '架构', 'gradle', 'MVVM', 'maven', 'Django'],
                   '前端开发': ['Chart.js', 'RequireJS', 'three.js', 'CoffeeScript', 'Backbone.js', 'SVG', 'NPM','React.js', 'Zepto.js', '交互设计', '响应式编程', 'Less', 'DNodeJS', 'Ajax', 'Express', 'SCSS', 'Sea.js', 'Grunt', 'Vuex', 'TypeScript', 'Canvas', '敏捷开发', '前端框架', 'Angular.js','Bootstrap', 'jQuery', '响应式设计', '前端', 'JavaScript', '前端框架', '设计模式', 'HTML', 'CSS','Node.js', 'Vue.js', 'ECMAScript 6'],
                   '智能硬件': ['蓝牙', '树莓派', 'Apple Watch', '安全', '嵌入式', '机器人', 'Mac'],
                   '理论基础': ['代码规范', '算法', '正则表达式', '机器学习', 'Caffe', '神经网络'],
                   '操作系统': ['macOS', 'CentOS', 'Ubuntu', 'Linux', '命令行', 'Windows', 'Apache Kylin'],
                   '综合应用': ['计算机视觉', 'Flask', '运维', '视觉设计', '游戏', '虚拟现实', 'Excel', '搜索引擎', '王者荣耀', '设计', '面试', '产品','微信', '全栈', '黑客', 'Chrome', 'Photoshop']}#大小类对应表

        #将所有文章读入内存
        articleList = []
        for i in collect2.find({},{"articleTitle":1,"articleUrl":1,"libraryName":1,"_id":0}):  #筛选字段
            articleList.append(i)

        # 初始化10个大标签 每个都是list 并对应存入
        self.tenDict = {'移动开发': [],
                   '云计算/大数据': [],
                   '编程语言': [],
                   '数据库': [],
                   '软件工程': [],
                   '前端开发': [],
                   '智能硬件': [],
                   '理论基础': [],
                   '操作系统': [],
                   '综合应用': [], }
        for i in articleList:
            libraryType = ''
            for j in self.dictBig:
                if (i['libraryName'] in self.dictBig[j]):
                    libraryType = j
                    break
            self.tenDict[libraryType].append(i)


    def run(self):
        '''
            开始推荐,每个大类随机推荐10条数据 共100条 存入数据库
        '''
        # self.collect.remove({})
        ii=0
        data=[]
        classfication={}
        for i in self.tenDict:
            classfication['classfication'+str(ii+1)]=[self.bigClass[ii],random.sample(self.tenDict[i], 10)]
            ii+=1
        for i in classfication.items():
            data.append(i)

        for i in classfication:
            print(i)
        self.collect.insert({'userName':"未登录用户",'recommendList':data,'nowTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


aa=guestClass()
aa.run()