<H3>1.redis支持的数据类型

	String字符串:
	格式: set key value
	String类型是二进制安全的。意思是redis的String可以包含任何数据。比如jpg图片或者序列化的对象。
	String类型是redis最近本的数据类型，一个键最大能存储512MB.
	
	Hash(哈希)：
	格式：hmset name key1 value1 key2 value2
	redis hash是一个键值(key=>value)对集合。
	redis hash是一个String类型的field的和value的映射表，hash特别适合用于存储对象。
	
	List（列表）：
	redis列表是简单的字符串列表，按照插入顺序排序，你可以添加一个元素到列表的头部或者尾部。
	格式：lpush name value
	在key对应的list的头部添加字符串元素。
	格式：rpush name value
	在key对应的list的尾部添加字符串元素。
	格式：lrem name index
	key对应list中删除count个和value相同的元素
	格式：llen name
	返回key对应的list的长度
	
	Set（集合）：
	格式：sadd name value
	redis的set是String类型的无需集合
	集合是通过哈希表实现的，所以，添加，删除，查找的复杂度都是O(1)。
	
	zset(sorted set:有序集合)：
	格式：zadd name score value
	redis zest和set一样也是string类型元素的集合，且不允许重复的成员。
	不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。
	zset的成员是唯一的，但分数（score）却可以重复。
	
	
<H3>2.什么是redis持久化？redis有哪几种持久化方式？优缺点是什么？

	持久化就是把内存的数据写到磁盘中去，防止服务宕机了内存数据丢失。
	redis提供了两种持久化方式：RDB(默认)和AOF
	
	RDB:
	rdb是redis database缩写，功能函数rdbSave（生成RDB文件）和rdbLoad（从文件加载内存）两个函数。

![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/interview/image-folder/redis-rdb.png)
	
	AOF:
	AOF是Append-only file缩写
	每当执行服务器（定时）任务或者函数时flushAppendOnlyFile函数都会被调用，这个函数执行一下两个工作。
	aof写入保存：
		1).WRITE:根据条件，将aof_buf中的缓存写入到AOF文件。
		2).SAVE:根据条件，调用fsync或fdatasync函数，将AOF文件保存到磁盘中。
![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/interview/image-folder/redis-aof.png)


	存储结构：内容是redis通讯协议（RESP）格式的命令文本存储。
	
	比较：
	1.AOF文件比RDB更新频率高，优先使用AOF还原数据。
	2.AOF比RDB更安全也更大。
	3.RDB性能比AOF好。
	4.如果两个都配了优先加载AOF。
	
	redis持久化存储更多知识：https://www.cnblogs.com/jasontec/p/9846725.html


<h3>3.什么时RESP协议？有什么特点？
	
	RESP是redis客户端和服务端之间使用的一种通讯协议。
	RESP的特点：实现简单、快速解析、可读性好。


<H3>4.redis中list底层实现有哪几种？有什么区别？

	列表对象的编码可以是ziplist或者linkedlist
	ziplist是一种压缩链表，它的好处是更能节省内存空间，因为它所存储的内容都是在连续的内存区域当中的。
	当列表对象元素不大，每个元素也不大的时候，就采用ziplist存储。但当数据量过大时就ziplist就不是那么
	好用了。因为为了保证他存储内容在内存中的连续性，插入的复杂度是O(N)，即每次插入都会进行realloc，对
	象机构中ptr所指向的就是一个ziplist，整个ziplist只需要malloc一次，他们在内存中是一块连续的区域。
	
	