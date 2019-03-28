```
# redis高可用方案 #

https://www.cnblogs.com/jaycekon/p/6237562.html

一、Sentinel的作用：
A、Master 状态监测
B、如果Master 异常，则会进行Master-slave 转换，将其中一个Slave作为Master，将之前的Master作为Slave 
C、Master-Slave切换后，master_redis.conf、slave_redis.conf和sentinel.conf的内容都会发生改变，即master_redis.conf中会多一行slaveof的配置，sentinel.conf的监控目标会随之调换 

二、Sentinel的工作方式:
1)：每个Sentinel以每秒钟一次的频率向它所知的Master，Slave以及其他 Sentinel 实例发送一个 PING 命令 
2)：如果一个实例（instance）距离最后一次有效回复 PING 命令的时间超过 down-after-milliseconds 选项所指定的值， 则这个实例会被 Sentinel 标记为主观下线。 
3)：如果一个Master被标记为主观下线，则正在监视这个Master的所有 Sentinel 要以每秒一次的频率确认Master的确进入了主观下线状态。 
4)：当有足够数量的 Sentinel（大于等于配置文件指定的值）在指定的时间范围内确认Master的确进入了主观下线状态， 则Master会被标记为客观下线 
5)：在一般情况下， 每个 Sentinel 会以每 10 秒一次的频率向它已知的所有Master，Slave发送 INFO 命令 
6)：当Master被 Sentinel 标记为客观下线时，Sentinel 向下线的 Master 的所有 Slave 发送 INFO 命令的频率会从 10 秒一次改为每秒一次 
7)：若没有足够数量的 Sentinel 同意 Master 已经下线， Master 的客观下线状态就会被移除。 
若 Master 重新向 Sentinel 的 PING 命令返回有效回复， Master 的主观下线状态就会被移除。

```

```
# redis api #

https://www.cnblogs.com/melonjiang/p/5342505.html

支持存储的value类型：string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）

string:
  get\set\range\bit\len\incr\decr\append
  
hash:
  get\set\len\keys\vals\exists\del\incr
  
list:
  lpush\rpush\linsert\lset\rpoplpush\brpoplpush\blpop\brpop
  lindex\llen\lrange\lpop\lrem\ltrim
  
set:
  sadd\smembers\scard\sismember\smove\spop\srandmember\srem
  sdiff\sdiffstore\sinter\sinterstore\sunion\sunionstore
  
zset:
  zadd\zcard\zcount\zincrby\zrange\zrevrange\zrank\zrevrank
  zscore\zrem\zremrangebyrank\zremrangebyscore
  zinterstore\zunionstore
  
other:
  type\keys\delete\exists\expire\rename\move\randomkey
```

```
# redis tips #

http://www.cnblogs.com/melonjiang/p/5342383.html

1. 连接池
2. 管道
3. 发布和订阅
```

```
Binary-safe strings
Lists(linked lists)
Sets
Sorted sets
Hashes
Bit arrays
HyperLogLogs
Streams


atomic increment
Common use cases for lists
    1.Remember the latest updates posted by users into a social network.
    2.Communication between processes, using a consumer-producer pattern where the producer pushes items into a list, and a consumer (usually a worker) consumes those items and executed actions. Redis has special list commands to make this use case both more reliable and efficient.
    
Sets
poker game
```
