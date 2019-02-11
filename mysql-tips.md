
```
ubuntu 16.04安装mysql:
  sudo apt-get install mysql-server
  
mysql开启多实例：
  端口、pid文件、socket文件、数据目录、日志目录
  安装位置：/usr/share/mysql
  配置目录：/etc/mysql
  数据目录：/var/lib/mysql/
  
  tips:
    apparmor & selinux
    
  步骤：
    1.创建数据目录并修改权限
      mkdir new_datadir
      chown -R mysql:mysql new_datadir
    2.修改配置文件
      port = 3307
      socket = new_datadir/mysqld.sock
      pid-file = new_datadir/mysqld.pid
      datadir = new_datadir
      log_error = new_datadir/error.log
    3.在apparmor中添加读写权限
      vim /etc/apparmor.d/usr.sbin.mysqld
      
      添加：
        new_datadir/ r,
        new_datadir/** rwk,
      
      service apparmor reload
    4.初始化数据库
      mysqld --initialize --datadir=new_datadir --user=mysql
      或
      mysql_install_db  --defaults-file=conf/3306my.cnf
    5.启动
      mysqld_safe --defaults-file=/etc/mysql/my1.cnf &
    6.初始化root密码
      mysqladmin -P 3306 -u root password '123123'
    
*****
    6.安全模式启动
      mysqld_safe --defaults-file = /etc/mysql/my1.cnf --skip-grant-tables
    7.无密码登陆
      mysql -S new_datadir/mysqld.sock
    8.手动update修改密码
      update user set authentication_string=password("123456") where user='root' and host='localhost';
      flush privileges;
    9.再次设置密码
      SET PASSWORD = PASSWORD('123456');  
```

```
mysql 主从复制：
  https://www.cnblogs.com/xiaochina/p/6886115.html
  
  1.开启binlog
    log-bin=mysql-bin             #开启二进制日志
    server-id=011                 #定义服务ID
  2.建立从复制账号
    grant replication slave on *.* to 'mysync'@'%' identified by '123456';             #所有IP
  3.查看Master信息
    show master status;
  4.进入mysql与master主机建立连接
    change master to master_host='172.24.0.130',master_port=3306,master_user='mysync',master_password='123456', master_log_file='mysql-bin.000003',master_log_pos=541;
  5.设置从库只读，启动从主机
    set global read_only=1;
    start  slave;
```

```
http://blog.csdn.net/xifeijian/article/details/20313977

mysql引擎：MyISAM、InnoDB

MyISAM引擎：
  表级锁 
      (表共享读锁（Table Read Lock）和表独占写锁（Table Write Lock）)
  可并发插入。
  concurrent_insert：2
  low-priority-updates
  max_write_lock_count：1

InnoDB引擎:
  行级锁
    共享锁和排他锁（lock in share mode and for update）
    延伸：乐观锁和悲观锁
    1. InnoDB行锁是通过给索引上的索引项加锁来实现的，这一点MySQL与Oracle不同，后者是通过在数据块中对相应数据行加锁来实现的。InnoDB这种行锁实现特点意味着：只有通过索引条件检索数据，InnoDB才使用行级锁，否则，InnoDB将使用表锁！
    2. 由于MySQL的行锁是针对索引加的锁，不是针对记录加的锁，所以虽然是访问不同行的记录，但是如果是使用相同的索引键，是会出现锁冲突的。
    3. 当表有多个索引的时候，不同的事务可以使用不同的索引锁定不同的行，另外，不论是使用主键索引、唯一索引或普通索引，InnoDB都会使用行锁来对数据加锁。
    4. 即便在条件中使用了索引字段，但是否使用索引来检索数据是由MySQL通过判断不同执行计划的代价来决定的，如果MySQL认为全表扫描效率更高，比如对一些很小的表，它就不会使用索引，这种情况下InnoDB将使用表锁，而不是行锁。因此，在分析锁冲突时，别忘了检查SQL的执行计划，以确认是否真正使用了索引。
    
  事务（TRANSACTION）
    四大基本属性：ACID属性
    带来的问题：脏读、丢失更新、不可重复读、幻读。
    事务隔离级别。（多版本并发控制MVCC）
    
  间隙锁（Next-Key锁）
    当我们用范围条件而不是相等条件检索数据，并请求共享或排他锁时，InnoDB会给符合条件的已有数据记录的索引项加锁；对于键值在条件范围内但并不存在的记录，叫做“间隙（GAP)”，InnoDB也会对这个“间隙”加锁，这种锁机制就是所谓的间隙锁（Next-Key锁）。
    一方面是为了防止幻读，以满足相关隔离级别的要求;另外一方面，是为了满足其恢复和复制的需要。
    带来的问题：会阻塞符合条件范围内键值的并发插入，这往往会造成严重的锁等待。
    
    MySQL的恢复机制要求：
        1. 在一个事务未提交前，其他并发事务不能插入满足其锁定条件的任何记录，也就是不允许出现幻读。（why？防止重复插入同一条数据？）
        2. CTAS操作给原表加锁（不确定（non-deterministic）的SQL，不推荐使用）
           tips：通过使用“select * from source_tab ... Into outfile”和“load data infile ...”语句组合来间接实现，采用这种方式MySQL不会给source_tab加锁
              
```

```
MySQL索引背后的数据结构及算法原理: http://blog.codinglabs.org/articles/theory-of-mysql-index.html
MySQL学习心得：http://www.cnblogs.com/lyhabc/p/3691555.html
```

expain出来的信息有10列，分别是id、select_type、table、type、possible_keys、key、key_len、ref、rows、Extra,下面对这些字段出现的可能进行解释：
二、select_type 表示查询中每个select子句的类型

(1) SIMPLE(简单SELECT,不使用UNION或子查询等)

(2) PRIMARY(查询中若包含任何复杂的子部分,最外层的select被标记为PRIMARY)

(3) UNION(UNION中的第二个或后面的SELECT语句)

(4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)

(5) UNION RESULT(UNION的结果)

(6) SUBQUERY(子查询中的第一个SELECT)

(7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，取决于外面的查询)

(8) DERIVED(派生表的SELECT, FROM子句的子查询)

(9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)

四、type

表示MySQL在表中找到所需行的方式，又称“访问类型”。

常用的类型有： ALL, index,  range, ref, eq_ref, const, system, NULL（从左到右，性能从差到好）

ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行

index: Full Index Scan，index与ALL区别为index类型只遍历索引树

range:只检索给定范围的行，使用一个索引来选择行

ref: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值

eq_ref: 类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件

const、system: 当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量,system是const类型的特例，当查询的表只有一行的情况下，使用system

NULL: MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。

十、Extra

该列包含MySQL解决查询的详细信息,有以下几种情况：

Using where:列数据是从仅仅使用了索引中的信息而没有读取实际的行动的表返回的，这发生在对表的全部的请求列都是同一个索引的部分的时候，表示mysql服务器将在存储引擎检索行后再进行过滤

Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询

Using filesort：MySQL中无法利用索引完成的排序操作称为“文件排序”

Using join buffer：改值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进能。

Impossible where：这个值强调了where语句会导致没有符合条件的行。

Select tables optimized away：这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行
