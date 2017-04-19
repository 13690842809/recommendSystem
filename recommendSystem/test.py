import urllib.request as ur
# set1={'a':['a'],'b':1}
# set1['c']=0
# if('a' in set1):
#     print('a')
# print(set1['a'].append('2'))
# print(set1.items())

#a
# dict_items([('b', 1), ('c', 0), ('a', 0)])

# import re
# str='/libraryList/js/jquery-3.0.0.min.js'
# if('js' in str):
#     print('a')
# print(a)

# import re
# str='/libraryList/agile'
# print(re.findall('\/libraryList\/(.*?)',str))articleUrl
'''
    通过推荐系统获得小标签list,去拿对应的平均条数数据
'''
# from pymongo import MongoClient
# import re
# conn = MongoClient(host="192.168.88.88", port=27017)
# db = conn.CSDN
# collect = db.ex_articleList
# my_library_code=[]
# my_library_name=[]
# # test=['RLV4K8pj', 'WoyLVXwZ', 'WDgcn73s', 'OjhSqCUG', 'lZAdrF1P', 'mrukFOw2', 'rd3jJ9VS']#测试的小标签 去数据库获取数据
# test=['WoyLVXwZ', 'zSJRE3b8', 'RLV4K8pj', 'nDh7iLlE', 'LeoMgzIb', 'lGaEujN6', 'mrukFOw2', 'cJvq2xrm',]
# eachTagNum=round(30/len(test))
# print(eachTagNum)
# data=[]
# for tag in test:
#     for i in collect.find({"libraryCode":tag},{"_id":0,"articleTitle":1,"articleUrl":1,"libraryName":1}).limit(eachTagNum): #多值查询并筛选字段
#         print(i)
#         data.append(i)
#     print('---')
# print(len(data))
'''
    内部链接测试
'''
#     my_library_code.append(i['libraryCode'])
#     my_library_name.append(i['libraryName'])
# a=['敏捷', 'Linux', '嵌入式开发', 'Hbase', '计算机网络', '软件测试', 'MySQL', '操作系统', 'CSS3', 'Git', 'Hadoop', '算法与数据结构', 'Oracle', 'JavaScript', '大型网站架构', 'Python', 'MongoDB', '微信开发', '人工智能', 'jQuery', 'Hive', 'Redis', '微服务', 'HTML5', 'React Native', '机器学习', '区块链', 'Docker', 'React', 'Java SE', '深度学习', 'Apache Spark', 'Node.js', '直播技术', 'iOS', 'OpenStack', 'AngularJS', 'Java EE', '信息无障碍', 'Android', 'Bluemix', '虚拟现实（VR）', 'PHP', 'Java', 'Objective-C', 'Go', '.NET', 'Swift', 'OpenCV', 'Cocos引擎', 'Scala', 'Unity3D']
# b=['agile', 'Linux', 'embeddeddevelopment', 'hbase', 'computernetworks', 'softwaretest', 'mysql', 'operatingsystem', 'css3', 'git', 'hadoop', 'datastructure', 'oracle', 'javascript', 'architecture', 'python', 'mongodb', 'wechat', 'ai', 'jquery', 'hive', 'redis', 'microservice', 'html5', 'reactnative', 'machinelearning', 'blockchain', 'docker', 'react', 'javase', 'deeplearning', 'spark', 'nodejs', 'liveplay', 'ios', 'openstack', 'angularjs', 'javaee', 'accessibility', 'android', 'bluemix', 'vr', 'php', 'java', 'objective-c', 'go', 'dotnet', 'swift', 'opencv', 'cocos', 'scala', 'unity3d']
#
# zip_dict = dict(zip(b, a))#code转name对照表
# # for i in zip_dict.items():
# #     print(i)
# print(zip_dict['datastructure'])               #不区分大小写查询 db.getCollection('ex_articleList').find({"libraryName":{$regex:"agile",$options:"$i"}})
# print('转换后',[zip_dict[x] for x in test])     #多value或查询 db.getCollection('ex_articleList').find({$or:[{"libraryName":"Hadoop"},{"libraryName":"敏捷"}]})
                                              #             db.getCollection('ex_articleList').find({"libraryName":{$in:["Hadoop","SQLite"]}})



