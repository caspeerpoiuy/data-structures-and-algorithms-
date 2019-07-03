<H3>Docker Image Command

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


<H3>Docker Container Command

	docker container attach                 Attach local standard input, output, and error streams to a running container
	docker container commit                 Create a new image from a container's changes
	docker container cp                     Copy files/folders between a container and the local filesystem
	docker container create                 Create a new container
	docker container diff                   Inspect changes to files or directories on a container's filesystem
	docker container exec                   Run a command in a running container
	docker container export                 Export a container's filesystem as a tar archive
	docker container inspect                Display detailed information on one or more containers
	docker container kill                   Kill one or more running containers
	docker container logs                   Fetch the logs of a container
	docker container ls                     List containers
	docker container pause                  Pause all processes within one or more containers
	docker container port                   List port mappings or a specific mapping for the container
	docker container prune                  Remove all stopped containers
	docker container rename                 Rename a container
	docker container restart                Restart one or more containers
	docker container rm                     Remove one or more containers
	docker container run                    Run a command in a new container
	docker container start                  Start one or more stopped containers
	docker container stats                  Display a live stream of container(s) resource usage statistics
	docker container stop                   Stop one or more running containers
	docker container top                    Display the running processes of a container
	docker container unpause                Unpause all processes within one or more containers
	docker container update                 Update configuration of one or more containers
	docker container wait                   Block until one or more containers stop, then print their exit codes


<H3>How to create a image:

	1.docker commit		base on exist container to create
	2.docker build		base on dockerfile to create
	3.docker import		base on local template import


<H3>What is the difference between  container and image：

	容器是镜像的一个运行实例，镜像是静态的只读文件，而容器带有运行时需要的可写文件层，同时，容器中的应用进程处于运行状态。


<H3>How to create a container

	docker [container] create
	
	
<H3>How to start a container:

	docker [container] start


<H3>create and start a container：

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


<H3>docker attach 和 docker exec:

	docker attach是进入到程序内pid为1的进程，即主进程
	docker exec [container-version] Command 	执行命令到容器内，不是pid为1的主进程``
	

<H3>docker file
<table>
	<tr>
		<td>
			command
		</td>
		<td>
			description
		</td>
	</tr>
	<tr>
		<td>
			ARG
		</td>
		<td>
			定义创建镜像过程中使用的变量
		</td>
	</tr>
	<tr>
		<td>
			FROM
		</td>
		<td>
			指定所创建的镜像的基础镜像
		</td>
	</tr>
	<tr>
		<td>
			LABEL
		</td>
		<td>
			为生成的镜像添加元数据标签信息
		</td>
	</tr>
	<tr>
		<td>
			EXPOSE
		</td>
		<td>
			声明镜像内服务监听的端口
		</td>
	</tr>
	<tr>
		<td>
			ENV
		</td>
		<td>
			指定环境变量
		</td>
	</tr>
	<tr>
		<td>
			ENTRYPOINT
		</td>
		<td>
			指定镜像的默认入口命令
		</td>
	</tr>
	<tr>
		<td>
			VOLUME
		</td>
		<td>
			创建一个数据卷挂载点
		</td>
	</tr>
	<tr>
		<td>
			USER
		</td>
		<td>
			指定运行容器时的用户名或UID
		</td>
	</tr>
	<tr>
		<td>
			WORKDIR
		</td>
		<td>
			配置工作目录
		</td>
	</tr>
	<tr>
		<td>
			ONBUILD
		</td>
		<td>
			创建子镜像时指定自动执行的操作指令
		</td>
	</tr>
		<tr>
		<td>
			STOPSIGNAL
		</td>
		<td>
			指定退出的信号值
		</td>
	</tr>
		<tr>
		<td>
			HEALTHCHECK
		</td>
		<td>
			配置所启动容器如何进行健康检查
		</td>
	</tr>
		<tr>
		<td>
			SHELL
		</td>
		<td>
			指定默认shell类型
		</td>
	</tr>
	</tr>
		<tr>
		<td>
			RUN
		</td>
		<td>
			运行指定命令
		</td>
	</tr>
	</tr>
		<tr>
		<td>
			CMD
		</td>
		<td>
			启动容器是指定默认执行的命令
		</td>
	</tr>
	</tr>
		<tr>
		<td>
			ADD
		</td>
		<td>
			添加内容到镜像
		</td>
	</tr>
	</tr>
		<tr>
		<td>
			COPY
		</td>
		<td>
			复制内容到镜像
		</td>
	</tr>
</table>


<H3>dockerfile中的命令COPY和ADD命令有什么区别？

	一般而言，虽然ADD与COPY在功能上类似，但是COPY是优选。
	因为它比ADD更透明。COPY仅支持将本地文件基本复制到容器中，而ADD具有一些功能（如仅限本地的tar提取和远程url支持）
	这些功能并不是很明显，因此，ADD的最佳用途是将本地tar文件自动提取到镜像中，如ADD rootfs.tar.gz

<H3>镜像相关
	
	1.如何备份系统中所有的镜像？
	答：
		首先，备份镜像列表可以使用docker images|awk 'NR>1{print $1":"$2}'| sort > images.list
		导出所有镜像为目前目录下文件，可以使用如下命令：
		while read img; do
			echo $img
			file="${img/\//-}"
			sudo docker save --output $file.tar $img
		done < images.list
		将本地镜像文件导入为docker镜像：
		while read img; do
			echo $img
			file="{img/\//-}"
			docker load < $file.tar
		done < images.list
		
	2.如何批量清理临时镜像文件？
	答：可以使用docker rmi ${docker images -q -f dangling=true}命令。
			
	3.如何删除所有本地的镜像？
	答：可以使用docker rmi -f ${docker images -q}命令。
			
	4.如何清理docker系统中的无用数据？
	答：可以使用docker system prune --volumes -f命令，这个命令会自动清理处于停止状态的容器、无用的网络和挂在卷、临时镜像和创建镜像缓存。
	
	5.如何查看镜像内的环境变量？
	答：可以使用docker run IMAGE env
	
	6.本地的镜像文件都存放在哪里？
	答：与docker相关的本地资源（包括镜像、容器）默认存放在/var/lib/docker/目录下。以aufs文件系统为例，其中container目录存放容器信息，
	graph目录存放镜像信息，aufs目录下存放具体的镜像层文件。
	
	7.构建docker镜像应该遵循那些原则？
	答：整体原则上，尽量保持镜像功能的明确和内容的精简，避免添加额外文件和操作步骤，要点包括：
	~尽量合并dockerfile命令，一边减少镜像层数，进而减少commit/run/rm次数，加快构建；
	~调整命令前后顺序，以便提高复用度及cache命中率，加速构建；(比如像RUN apt-get -y update这类大多镜像都需要用到命令应该放在上面，以便
	跨镜像服用。然而像WORKDIR、CMD、ENV、ADD这些可能导致cache miss的命令应该放在底部)
	~尽量选取满足需求但较小的基础系统镜像，例如大部分时候可以选择debian:wheezy或debian:jessie镜像，仅有不足百兆大小；
	~清理编译生成的文件、安装包的缓存等临时文件；
	~安装各个软件时候要指定准确的版本号，并避免引入不需要的依赖；
	~从安全角度考虑，应用要尽量使用系统的库和依赖；
	~如果安装应用时候需要配置一些特殊的环境变量，在安装后要还原不需要保持的变量值；
	~使用dockerfile创建镜像时候要添加.dockerignore文件或使用干净的工作目录；
	~区分编译环境容器和运行时环境容器，使用多阶段镜像创建。
	
	8.碰到网络问题，无法pull镜像，命令行指定http_proxy无效，怎么办？
	答：在docker配置文件中添加export http_proxy="http://<PROXY_HOST>:<PROXY_PORT>"，之后重启docker服务即可。
	
	
<H3>容器相关
	
	1.容器退出后，通过docker ps命令查看不到，数据会丢失吗？
	答：容器退出后会处于终止（exited）状态，此时可以通过docker ps -a查看。其中的数据也不会丢失，还可以通过docker [container] start
	命令来启动它。只有删除掉容器才会清除所有数据。
	
	2.如何停止所有正在运行的容器？
	答：可以使用docker [container] stop ${docker ps -q}命令。
	
	3.如何批量清理所有的容器，包括处于运行状态和停止状态的？
	答：可以使用docker [container] rm -f ${docker ps -qa}命令。			
	
	4.如何获取某个容器的PID信息？
	答：可以使用docker [container] inspect --format '{{ .State.Pid }}' <CONTAINER ID OR NAME> 命令。
	
	5.如何获取某个容器的IP地址？
	答：可以使用docker [container] inspect --format '{{ .NetworkSettings.IPAddress }}' <CONTAINER ID OR NAME> 命令。
	
	6.如何临时退出一个正在交互的容器的终端，而不终止它？
	答：按CTRL+P + CTRL+Q，如果按CTRL+C往往会让容器内应用进程终止，进而会终止容器。
			
	7.可以在一个容器中同事运行多个应用进程吗？
	答：一般不推荐在同一个容器内运行多个应用进程。如果有类似需求，可以通过一些额外的进程管理机制，比如supervisord，来管理所运行的进程。
	
	8.如何控制容器占用系统资源(CPU、内存)的份额？
	答：在使用docker [container]	create命令创建容器或使用docker [container] run创建并启动容器的时候，可以使用-c|-cpu-shares[=0]	
	参数来调整使用cpu的权重；使用-m|-memory[=MEMORY]参数来调整容器使用内存的大小。
	
	
<H3>docker run动作
			
	
	当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：
		检查本地是否存在指定的镜像，不存在就从公有仓库下载
		利用镜像创建并启动一个容器
		分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
		从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
		从地址池配置一个 ip 地址给容器
		执行用户指定的应用程序
		执行完毕后容器被终止
			
			
			
			
			
			
			
			
			
			1
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			