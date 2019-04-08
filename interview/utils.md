<H3>1.HTTP和HTTPS区别

	HTTP:基于TCP,用于从WWW服务器传输超文本到本地浏览器的传输协议，它可以使浏览器更加高效，
	是网络传输减少。
	HTTPS:是以安全为目标的HTTP通道，简单讲是HTTP的安全版，即HTTP加入SSL层，HTTPS的安全
	基础是SSL，因此加密的详细内容就需要SSL。
	HTTPS协议的主要作用可以分为两种：一种是建立一个信息安全通道，来保证数据传输的安全；另一
	种就是确认网站的真实性。
	
	HTTP协议传输的数据都是未加密的，也就是明文的，因此使用HTTP协议传输隐私信息非常不安全，
	为了保证这些隐私数据能加密传输，于是设计了SSL协议用于对HTTP协议传输的数据进行加密传输、
	身份认证的网络协议，要比HTTP协议安全。
	
	HTTP和HTTPS的区别主要如下：
	1.HTTPS协议需要到CA申请证书，一般免费证书比较少，因而需要一定费用。
	2.HTTP是超文本传输协议，信息是明文传输，HTTPS则是具有安全性的SSL加密传输协议。
	3.HTTP和HTTPS使用的是完全不同的连接方式，用的端口也不一样，前者是80，后者是443。
	4.HTTP的连接很简单，是无状态的；HTTPS协议是由SSL+HTTP协议构建的可进行加密传输、身份
	认证的网络协议，比HTTP协议安全。
	

<H3>2.HTTPS的工作原理

	客户端在使用HTTPS方式与web服务器通信时有以下几个步骤。
	1.客户使用HTTPS的url访问web服务器，要求与web服务器建立SSL连接。
	2.web服务器收到客户端请求后，会将网站的证书信息（证书中包含公钥）传送一份到客户端。
	3.客户端的浏览器与web服务器开始协商SSL连接的安全等级，也就是信息加密的等级。
	4.客户端的浏览器根据双方同意的安全等级，建立会话密钥，然后利用网站的公钥将会话密钥加密，并传送给网站。
	5.web服务器利用自己的私钥解密出会话密钥。
	6.web服务器利用会话密钥加密与客户端之间的通信。
![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/interview/image-folder/https-procedure1.png)
![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/interview/image-folder/https-procedure.png)


<H3>3.HTTPS的优缺点

	主要有以下几个好处：
	1.使用HTTPS协议可认真用户和服务器，确保数据发送到正确的客户机和服务器；
	2.HTTPS协议是SSL+HTTP协议构建的可进行加密传输、身份认证的网络协议，要比HTTP协议安全，可防止数据在传输过程中不被窃取、改变、确保数据的完整性。
	3.HTTPS是现行架构下最安全的解决方案，虽然不是绝对安全，但它大幅增加了中间人攻击的成本。
	4.采用HTTPS加密的网站在搜索结果中的排名会更高。
	
	
	不足之处：
	1.HTTPS协议握手阶段比较耗时，会使页面加载时间延长近50%，增加10%到20%的耗电。
	2.HTTPS连接缓存不如HTTP高效，会增加数据开销和功耗，甚至已有的安全措施也会因此而受到影响。
	3.SSL证书需要钱，功能越强大的证书费用越高，个人网站、小网站没有必要一般不会用。
	4.SSL证书通常需要绑定IP，不能在同一IP上绑定多个域名，IPv4资源不可能支撑这个消耗。
	5.HTTPS协议的加密范围也比较有限，在黑客攻击、拒绝服务攻击、服务器劫持等方面几乎起不到什么作用。最关键的，SSL证书的信用链体系并不安全，特别是在
	某些国家可以控制CA证书的情况下，中间人攻击一样可行。
	

<H3>4.HTTP切换到HTTPS

	如果需要将网站从HTTP切换到HTTPS到底该如何实现呢？
	这里需要将页面中所有的链接，例如js，css，图片等等链接都由HTTP改为HTTPS。
	这里虽然将HTTP切换为了HTTPS，还是建议保留HTTP。所以我们在切换的时候可以做HTTP和HTTPS的兼容，具体实现方式是，去掉页面链接中的HTTP头部，这
	样可以自动匹配HTTP头和HTTPS头。例如：将http://www.baidu.com改为//www.baidu.com。然后当用户从HTTP的入口进入访问页面时，页面就是HTTP
	如果用户是从HTTPS的入口进入访问页面，页面即是HTTPS的。
	

<H3>5.HTTP请求方法都有什么

	根据HTTP标准，HTTP请求可以使用多种请求方法。
	HTTP1.0定义了三种请求方法：GET,POST,HEAD
	HTTP1.1新增了五分钟请求方法：OPTIONS,PUT,DELETE,TRACE,CONNECT方法。
	1.GET   请求指定的页面信息，并返回实体主体。
	2.HEAD  类似于GET请求，只不过返回的响应中没有具体的内容，用于获取包头。
	3.POST  向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修
	改。
	4.PUT   从客户端向服务器传送的数据取代指定的文档的内容。
	5.DELETE    请求服务器删除指定的页面。
	6.CONNECT   HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。
	7.OPTIONS   允许客户端查看服务器的性能。
	8.TRACE 回显服务器收到的请求，主要用于测试或诊断。
	
	
<h3>6.HTTP常见请求头

	1.HOST(主机和端口号) 
	2.Connection(链接类型)
	3.Upgrade-Insecure-Resquests(升级为HTTPS请求)
	4.User-Agent(浏览器名称)
	5.Accept(传输文件类型)
	6.Referer(页面跳转处)
	7.Accept-Encoding(文件编解码格式)
	8.Cookie(Cookie)
	9.x-requested-with(是Ajax异步请求)
	10.Content-Length(表示请求消息正文的长度)
	
	
<H3>7.Restful风格的请求
	
	HEAD(SELECT)只获取某个资源的头部信息
	GET(SELECT)获取资源
	POST(CREATE)创建资源
	PATCH(UPDATE)更新资源的部分属性（很少用，一般用POST代替）
	PUT(UPDATE)更新资源，客户端需要提供新建资源的所有属性
	DELETE(DELETE)删除资源

	POST与PUT区别
	POST:用来创建一个子资源，POST方法不是幂等的，多次执行，将导致多条相同的数据被创建，而这些数据除了自增长ID外有着相同的数据，
	除非你的系统实现了额外的数据唯一性检查。
	PUT:如果已存在就替换，没有就新增；因此PUT方法一般会用来更新一个已知的资源，除非在创建前，你完全知道自己要创建的对象的URI。
	
	PATCH方法是新引入的，是对PUT方法的补充，用来对已知资源进行局部更新。
	
	
	
	
	
	
	
	
	
	



















