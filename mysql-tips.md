
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
    5.启动
      mysqld_safe --defaults-file=/etc/mysql/my1.cnf
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
