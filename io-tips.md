```
参考：http://blog.csdn.net/baixiaoshi/article/details/48708347

高性能IO模型浅析
    1.同步阻塞IO
    2.同步非阻塞IO
    3.异步阻塞IO（IO多路复用）（Reactor设计模式）
      select(windows支持，有最大文件描述符数量限制，效率没有epoll高)
      poll
      epoll（不支持windows，无最大文件描述符限制，效率高）
    4.异步非阻塞IO（需要内核支持，比较少见）（Proactor设计模式）
    
市面上的nginx、tornado是IO多路复用。
```
