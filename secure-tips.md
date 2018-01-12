```
总结 XSS 与 CSRF 两种跨站攻击: https://blog.tonyseek.com/post/introduce-to-xss-and-csrf/

SQL注入：
  漏洞：拼接字符串的方式来构造动态 SQL 语句
  解决方法： 参数化查询
  
XSS：跨站脚本（Cross-site scripting）
  漏洞：XSS 全称“跨站脚本”，是注入攻击的一种。其特点是不对服务器端造成任何伤害，而是通过一些正常的站内交互途径，
  例如发布评论，提交含有 JavaScript 的内容文本。这时服务器端如果没有过滤或转义掉这些脚本，作为内容发布到了页面上，
  其他用户访问这个页面的时候就会运行这些脚本。
  解决方法：过滤用户输入、开启模版自动转义
  
CSRF：跨站请求伪造（Cross-site request forgery）
  与XSS的关系：XSS 是实现 CSRF 的诸多途径中的一条，但绝对不是唯一的一条。
  漏洞：伪造请求，冒充用户在站内的正常操作
  解决方案：请求令牌
  

浏览器都有一个同源策略，其限制之一就是第一种方法中我们说的不能通过ajax的方法去请求不同源中的文档。 它的第二个限制是浏览器中不同域的框架之间是不能进行js的交互操作的。
跨域：https://www.cnblogs.com/2050/p/3191744.html
  借助JSONP协议：
    1、通过jsonp跨域，
       缺点：需要服务端支持
     
  借助iframe：
    2、通过修改document.domain来跨子域
       缺点：主域必须相同

    3、使用window.name来进行跨域
       缺点：window.name的值只能是字符串的形式

    4.使用HTML5中新引进的window.postMessage方法来跨域传送数据
       缺点：IE6、IE7不支持
```
