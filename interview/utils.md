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























