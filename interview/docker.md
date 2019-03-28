<H3>**Docker Image Command**

	docker image pull               	pull a image from docker hub
	docker image build                      build an image from docker file
	docker image history                    show the history of an image 
	docker image import                     display detailed of an image
	docker image load                       load an image from a tar archive or STDIN
	docker image ls                         list images
	docker image prune                      remove unused images
	docker image pull                       pull an image or a repository from a registry
	docker image push                       push an image or a repository to a registry
	docker image rm                         Remove one or more images
	docker image save                       Save one or more images to a tar archive (streamed to STDOUT by default)
	docker image tag                        Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE


	
<H3>**How to create a image???:**

	1.docker commit		base on exist container to create
	2.docker build		base on dockerfile to create
	3.docker import		base on local template import

<H3>**What is the difference between  container and image：**

	容器是镜像的一个运行实例，镜像是静态的只读文件，而容器带有运行时需要的可写文件层，同时，容器中的应用进程处于运行状态。

<H3>**How to create a container：**

	docker [container] create
	
<H3>**How to start a container：**

	docker [container] start

<H3>**create and start a container：**

	docker [container] run;	
	docker run = docker create + docker start

	docker run操作：
		检查本地是否存在指定的镜像，不存在就从共有仓库下载；
		利用镜像创建容器，并启动该容器；
		分配一个文件系统给容器，并在只读的镜像层外面挂载一层可读可写层；
		从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中；
		从网桥的地址池配置一个IP地址给容器；
		执行用户指定的应用程序；
		执行完毕后容器被自动终止；

	docker [container] run [option] image [command]

	[option]
	-a		是否绑定到标准输入、输出和错误
	-d 		是否在后台运行容器，默认为否
	-i   	保持标准输入打开，默认为false
	-t 		是否分配一个伪终端，默认为false
	-v 		挂载主机上的文件卷到容器内
	-w		容器内的默认工作目录
	-e  	指定容器内环境变量
	-h 		指定容器内的主机名

	docker run的时候因为命令无法正常执行容器会出错，直接退出，此时可以查看退出的错误代码。
	常见错误码包括：
		125：Docker daemon执行出错，例如指定了不支持的docker命令参数
		126：所指定命令无法执行，例如权限出错
		127：容器内命令无法找到



<H3>**docker attach 和 docker exec**

	docker attach是进入到程序内pid为1的进程，即主进程
	docker exec [container-version] Command 	执行命令到容器内，不是pid为1的主进程``