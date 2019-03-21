```
user www-data;
worker_processes auto;
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000;
pid /run/nginx.pid;
worker_rlimit_nofile 2048;
error_log /www/log/nginx_error.log crit;

events {
        worker_connections 1024;
        multi_accept on;
        accept_mutex on;
        use epoll;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;    #zero-copy
        tcp_nopush on;  #
        tcp_nodelay on; #Nagle算法&延迟 ACK
        
        types_hash_max_size 2048;
        server_tokens off;

        server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        #access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;
        gzip_http_version 1.1;
        gzip_disable "msie6";
        gzip_comp_level 6;
        gzip_min_length 2k;
        gzip_proxied any;
        gzip_buffers 16 8k;
        gzip_vary on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        # Configure timeouts
        # if timeout raise 408
        client_body_timeout   12;
        client_header_timeout 12;
        send_timeout          10;

        #Buffers
        #if too big raise 414
        client_body_buffer_size       16K;
        client_max_body_size          8m;
        
        #if too big raise 400
        client_header_buffer_size     4k;
        large_client_header_buffers   2 4k;
        
        #keepalive
        keepalive_disable msie6; 
        keepalive_requests 100000;
        keepalive_timeout 65 60;
        
        #open_file_cache
        open_file_cache max=102400 inactive=20s;
        open_file_cache_valid 30s;
        open_file_cache_min_uses 1;
        open_file_cache_errors on;
        
        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
        
        server {
            location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
                expires 1M;
                add_header Cache-Control public;
                add_header Pragma public;
                add_header Vary Accept-Encoding; #CDN
            }
        }
}
```

```
=  #用于标准uri前，需要请求字串与uri完全匹配，如果匹配成功就停止向下匹配并立即处理请求。
~  #区分大小写
~*  #不区分大写
!~  #区分大小写不匹配
!~* #不区分大小写不匹配 
^  #匹配以什么开头
$  #匹配以什么结尾
\  #转义字符。可以转. * ?等
*  #代表任意长度的任意字符

-f和!-f #用来判断是否存在文件
-d和!-d #用来判断是否存在目录
-e和!-e #用来判断是否存在文件或目录
-x和!-x #用来判断文件是否可执行

200 #请求成功，即服务器返回成功
301 #永久重定向
302 #临时重定向
403 #禁止访问，一般是服务器权限拒绝
400 #错误请求，请求中有语法问题，或不能满足请求。  
403 #服务器权限问题导致无法显示
404 #服务器找不到用户请求的页面
500 #服务器内部错误，大部分是服务器的设置或内部程序出现问题
501 #没有将正在访问的网站设置为浏览器所请求的内容
502 #网关问题，是代理服务器请求后端服务器时，后端服务器不可用或没有完成 相应网关服务器，这通常是反向代理服务器下面的节点出问题导致的。
503 ＃服务当前不可用，可能是服务器超载或停机导致的，或者是反向代理服务器后面没有可以提供服务的节点。
504 #网关超时，一般是网关代理服务器请求后端服务器时，后端服务器没有在指定的时间内完成处理请求，多数是服务器过载导致没有在特定的时间内返回数据给前端代理服务器。
505 #该网站不支持浏览器用于请求网页的ＨＴＴＰ协议版本（最为常见的是ＨＴＴＰ/1.1）
```

```
sysctl.conf针对IPv4内核的7个参数的配置优化：
#每个网络接口的处理速率比内核处理包的速度快的时候，允许发送队列的最大数目。
net.core.netdev_max_backlog = 102400

#用于调节系统同时发起的TCP连接数，默认值一般为128，在客户端存在高并发请求的时候，128就变得比较小了，可能会导致链接超时或者重传问题。
net.core.somaxconn = 102400

设置系统中做多允许多少TCP套接字不被关联到任何一个用户文件句柄上，如果超出这个值，没有与用户文件句柄关联的TCP套接字将立即被复位，同时给出警告信息，这个值是简单防止DDOS（Denial of service）的攻击，在内存比较充足的时候可以设置大一些：
net.ipv4.tcp_max_orphans = 102400

用于记录尚未收到客户度确认消息的连接请求的最大值，一般要设置大一些：
net.ipv4.tcp_max_syn_backlog =  102400

#用于设置时间戳，可以避免序列号的卷绕，有时候会出现数据包用之前的序列号的情况，此值默认为1表示不允许序列号的数据包，对于Nginx服务器来说，要改为0禁用对于TCP时间戳的支持，这样TCP协议会让内核接受这种数据包，从而避免网络异常，如下：
net.ipv4.tcp_timestamps = 0

#用于设置内核放弃TCP连接之前向客户端发生SYN+ACK包的数量，网络连接建立需要三次握手，客户端首先向服务器发生一个连接请求，服务器收到后由内核回复一个SYN+ACK的报文，这个值不能设置过多，会影响服务器的性能，还会引起syn攻击：
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_syn_retries = 1

timewait 的数量，默认是180000。
net.ipv4.tcp_max_tw_buckets = 6000

允许系统打开的端口范围。
net.ipv4.ip_local_port_range = 1024 65000

启用timewait 快速回收。
net.ipv4.tcp_tw_recycle = 1

开启重用。允许将TIME-WAIT sockets 重新用于新的TCP 连接。
net.ipv4.tcp_tw_reuse = 1

开启SYN Cookies，当出现SYN 等待队列溢出时，启用cookies 来处理。
net.ipv4.tcp_syncookies = 1
```
