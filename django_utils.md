
```
Django-基于Python的Web开发架构，拥有与SQL查询语句完全分离的数据库处理机制，它可以让不懂SQL语法的开发人员轻松处理数据库内容（包括insert、delete、update等等常用功能）。
该文档的需求出发点为：
    当有web应用的后台数据需要批量更新时，通常的解决方案是：
    1. 将文件整理成数据库table完全适配的格式并使用load（mysql）或copy（postgres）导入
    2. 当文件内容需要进行预处理时，这需要一个程序调用数据库接口，边处理边存入
    基于解决方案2，将有以下棘手问题：
    1. 不懂 SQL语言
    2. 需要重新学习psycopg2、MySQLdb等接口用法
    3. 不同的数据库需要了解不同的接口、不同的语法
```



```
具体如下：
#! /usr/local/bin/python
import psycopg2 ,sys,re
#import MySQLdb ,sys,re
ifile=sys.argv[1]
itype=sys.argv[2]
conn = psycopg2.connect(database="Django", user="django", password="******", host="localhost", port="5432") ##Postgres接口，连接数据库
#conn = MySQLdb.connect(host='localhost',user='django',passwd='******',db='Django',port=3306)
cur = conn.cursor() ##MYSQL接口
File=file(ifile,'r')
for line in File.readlines():
array=line.split("\t")
for i in range(0,len(array)):
if re.search(r'^\s*NULL\s*$',array[i]): 
array[i]="" 
cur.execute('INSERT INTO "Disease_disease"(id,"Name","Count","Description") VALUES(%s,%s,%s,%s)', (array[0],array[1],array[2],array[3]))  ##Postgres，提交SQL insert查询语句
#cur.execute('INSERT INTO Disease_disease(id,Name,Count,Description) VALUES(%s,%s,%s,%s)', (array[0],array[1],array[2],array[3]))  ##MYSQL
conn.commit()
cur.close()
conn.close()
```


```
Django 解决方案：
直接调用django模块及其配置文件，直接使用django语法并处理数据库
具体如下：
#! /usr/local/bin/python
import sys, re 
sys.path.append("/home/zhuying/WebSite") ## 设置目录，即后台代码Project目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebSite.settings")  ##调用该Project的配置文件
from OneKP.models import *  ##调用OneKP这个App的数据库模型
family=Family.objects.get(id=1)
family.Name="Unknown"
family.Description="Unknown"
family.save()
注：该程序为普通python程序，与django web应用后台程序无关
更高的价值：

该解决方案更高的价值并不显现于单表和单记录的查询和处理，而在于复杂数据库模型下，不同表之间的外键索引联系的联动处理。
```
