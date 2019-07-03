

# 第1章　虚拟化与云计算

​	在计算机领域，虚拟化指创建某事物的虚拟（而非实际）版本，包括虚拟的计算机硬件平台、存储设备，以及计算机网络资源）可见，虚拟化是一种资源管理技术，它将计算机的各种实体资源（CPU、内存、存储、网络等）予以抽象和转化出来，并提供分割、重新组合，以达到最大化利用物理资源的目的

## 1.1　虚拟化技术

​	**虚拟化技术**：计算元件在虚拟的基础上而不是真实的基础上，是指一个为了简化管理、优化资源的解决方案。

​	**VMM：Virtual Machine Monito**r（VMM，虚拟机监控器），也称为Hypervisor层，就是为了达到虚拟化而引入的一个软件层。它向下掌控实际的物理资源（相当于原本的操作系统）；向上呈现给虚拟机N份逻辑的资源。为了做到这一点，就需要将虚拟机对物理资源的访问“偷梁换柱”——截取并重定向，让虚拟机误以为自己是在独享物理资源。![图1-1物理资源虚拟化示意图](.\kvm实践\1-1物理资源虚拟化示意图.jpg)

​	虚拟机监控器运行的环境，也就是真实的物理平台，称之**宿主机**。而虚拟出来的平台称**客户机**（Guest），里面运行的系统对应的成为客户机操作系统（GuestOS）。

### 1.1.1　软件虚拟化和硬件虚拟化(软件虚拟化Qemu,硬件VMM)

**1.软件虚拟化技术**

​	软件虚拟化，顾名思义，就是通过软件模拟来实现VMM层，通过纯软件的环境来模拟执行客户机里的指令。
​	最纯粹的软件虚拟化实现当属QEMU。在没有启用硬件虚拟化辅助的时候，它通过软件的二进制翻译仿真出目标平台呈现给客户机，客户机的每一条目标平台指令都会被QEMU截取，并翻译成宿主机平台的指令，然后交给实际的物理平台执行。由于每一条都需要这么操作一下，其虚拟化性能是比较差的，同时其软件复杂度也大大增加。但好处是可以呈现各种平台给客户机，只要其二进制翻译支持。

**2.硬件虚拟化技术**

​	硬件虚拟化技术就是指计算机硬件本身提供能力让客户机指令独立执行，而不需要（严格来说是不完全需要）VMM截获重定向。
​	以x86架构为例，它提供一个略微受限制的硬件运行环境供客户机运行（non-rootmod），在绝大多数情况下，客户机在此受限环境中运行与原生系统在非虚拟化环境中运行没有什么两样，不需要像软件虚拟化那样每条指令都先翻译再执行，而VMM运行在root mode，拥有完整的硬件访问控制权限。仅仅在少数必要的时候，某些客户机指令的运行才需要被VMM截获并做相应处理，之后客户机返回并继续在non-root mode中运行。可以见，硬件虚拟化技术的性能接近于原生系统，并且，极大地简化了VMM的软件设计架构。Intel从2005年就开始在其x86 CPU中加入硬件虚拟化的支持——Intel VirtualizationTechnology，简称**Intel VT.**

### 1.1.2　半虚拟化和全虚拟化

​	最理想的虚拟化的两个目标如下：
1）客户机完全不知道自己运行在虚拟化环境中，还以为自己运行在原生环境里。
2）完全不需要VMM介入客户机的运行过程。

**1.半虚拟化**

让客户机意识到自己是运行在虚拟化环境里，并做相应修改以配合VMM，这就是半虚拟化（Para-Virtualization）。一方面，可以提升性能和简化VMM软件复杂度；另一方面，也不需要太依赖硬件虚拟化的支持，从而使得其软件设计（至少是VMM这一侧）可以跨平台且是优雅的。“本质上，准虚拟化弱化了对虚拟机特殊指令的被动截获要求，将其转化成客户机操作系统的主动通知。但是，准虚拟化需要修改客户机操作系统的源代码来实现主动通知。”典型的半虚拟化技术就是virtio，使用virtio需要在宿主机/VMM和客户机里都相应地装上驱动。

**2.全虚拟化**

全虚拟化（Full Virtualization）坚持第一个理想化目标：客户机的操作系统完全不需要改动。敏感指令在操作系统和硬件之间被VMM捕捉处理，客户操作系统无须修改，所有软件都能在虚拟机中运行。因此，全虚拟化需要模拟出完整的、和物理平台一模一样的平台给客户机，这在达到了第一个目标的同时也增加了虚拟化层（VMM）的复杂度。

### 1.1.3　Type1和Type2虚拟化

从软件框架的角度上，根据虚拟化层是直接位于硬件之上还是在一个宿主操作系统之上，将虚拟化划分为Typel和Type2，如图1-2所示。![](.\kvm实践\1-2类型1和类型2的hypervisor.jpg)

Type1（类型1）Hypervisor也叫native或bare-metal Hypervisor。这类虚拟化层直接运行在硬件之上，没有所谓的宿主机操作系统。它们直接控制硬件资源以及客户机。典型地如Xen和VMware ESX。
Type2（类型2）Hypervisor运行在一个宿主机操作系统之上，如VMwareWorkstation；或系统里，如KVM。这类Hypervisor通常就是宿主机操作系统的一个应用程序，像其他应用程序一样受宿主机操作系统的管理。比如VMware Workstation就是运行在Windows或者Linux操作系统上的一个程序而已。客户机是在宿主机操作系统上的一个抽象，通常抽象为进程。

## 1.2　KVM简介

**KVM全称是Kernel-based Virtual Machine**，即基于内核的虚拟机，是采用硬件虚拟化技术的全虚拟化解决方案。

### 1.2.1　KVM的功能概览

KVM从诞生开始就定位于基于硬件虚拟化支持的全虚拟化实现。它以内核模块的形式加载之后，就将Linux内核变成了一个Hypervisor，但硬件管理等还是通过Linux kernel来完成的，所以它是一个典型的Type 2 Hypervisor，如图1-3所示。![](.\kvm实践\图1-3KVM功能框架.jpg)

一个KVM客户机对应于一个Linux进程，每个vCPU则是这个进程下的一个线程，还有单独的处理IO的线程，也在一个线程组内。所以，宿主机上各个客户机是由宿主机内核像调度普通进程一样调度的，即可以通过Linux的各种进程调度的手段来实现不同客户机的权限限定、优先级等功能。

### 1.2.2、KVM的功能特性

1、**内存管理**

KVM依赖Linux内核进行内存管理。上面提到，一个KVM客户机就是一个普通的Linux进程，所以，客户机的“物理内存”就是宿主机内核管理的普通进程的虚拟内存。进而，Linux内存管理的机制，如大页、KSM（Kernel Same Page Merge，内核的同页合并）、NUMA（Non-Uniform Memory Arch，非一致性内存架构）[2]、通过mmap的进程间共享内存，统统可以应用到客户机内存管理上。

早期时候，客户机自身内存访问落实到真实的宿主机的物理内存的机制叫影子页表（Shadow Page Table）。KVM Hypervisor为每个客户机准备一份影子页表，与客户机自身页表建立一一对应的关系。客户机自身页表描述的是GVA→GPA[3]的映射关系；影子页表描述的是GPA→HPA的映射关系。当客户机操作自身页表的时候，KVM就相应地更新影子页表。比如，当客户机第一次访问某个物理页的时候，由于Linux给进程的内存通常都是拖延到最后要访问的一刻才实际分配的，所以，此时影子页表中这个页表项是空的，KVM Hypervisor会像处理通常的缺页异常那样，把这个物理页补上，再返回客户机执行的上下文中，由客户机继续完成它的缺页异常。

影子页表的机制是比较拗口，执行的代价也是比较大的。所以，后来，这种靠软件的GVA→GPA→HVA→HPA的转换被硬件逻辑取代了，大大提高了执行效率。这就是Intel的EPT或者AMD的NPT技术，两家的方法类似，都是通过一组可以被硬件识别的数据结构，不用KVM建立并维护额外的影子页表，由硬件自动算出GPA→HPA。现在的VM默认都打开了EPT/NPT功能。

**2.存储和客户机镜像的格式**

严格来说，这是QEMU的功能特性。

KVM能够使用Linux支持的任何存储来存储虚拟机镜像，包括具有IDE、SCSI和SATA的本地磁盘，网络附加存储（NAS）（包括NFS和SAMBA/CIFS），或者支持iSCSI和光线通道的SAN。多路径I/O可用于改进存储吞吐量和提供冗余。

由于KVM是Linux内核的一部分，它可以利用所有领先存储供应商都支持的一种成熟且可靠的存储基础架构，它的存储堆栈在生产部署方面具有良好的记录。

KVM还支持全局文件系统（GFS2）等共享文件系统上的虚拟机镜像，以允许客户机镜像在多个宿主机之间共享或使用逻辑卷共享。磁盘镜像支持稀疏文件形式，支持通过仅在虚拟机需要时分配存储空间，而不是提前分配整个存储空间，这就提高了存储利用率。

**KVM的原生磁盘格式为QCOW2，它支持快照，允许多级快照、压缩和加密。**

**3.实时迁移**
KVM支持实时迁移，这提供了在宿主机之间转移正在运行的客户机而不中断服务的能力。实时迁移对用户是透明的，客户机保持打开，网络连接保持活动，用户应用程序也持续运行，但客户机转移到了一个新的宿主机上。除了实时迁移，KVM支持将客户机的当前状态（快照，snapshot）保存到磁盘，以允许存储并在以后恢复它。

**4.设备驱动程序**
KVM支持混合虚拟化，其中半虚拟化的驱动程序安装在客户机操作系统中，允许虚拟机使用优化的I/O接口而不使用模拟的设备，从而为网络和块设备提供高性能的I/O。KVM使用的半虚拟化的驱动程序是IBM和Redhat联合Linux社区开发的VirtIO标准；它是一个与Hypervisor独立的、构建设备驱动程序的接口，允许多种Hypervisor使用一组相同的设备驱动程序，能够实现更好的对客户机的互操作性。同时，KVM也支持Intel的VT-d技术，通过将宿主机的PCI总线上的设备透传（passthrough）给客户机，让客户机可以直接使用原生的驱动程序高效地使用这些设备。这种使用是几乎不需要Hypervisor的介入的。

**5.性能和可伸缩性**
KVM也继承了Linux的性能和可伸缩性。KVM在CPU、内存、网络、磁盘等虚拟化性能上表现出色，大多都在原生系统的95%以上。KVM的伸缩性也非常好，支持拥有多达288个vCPU和4TB RAM的客户机，对于宿主机上可以同时运行的客户机数量，软件上无上限。

[3] GVA：Guest Virtual Address，客户机虚拟地址。GPA：Guest Physical Address，客户
机物理地址。HVA：Host Virtual Address，宿主机虚拟地址。HPA：Host Physical
Address，宿主机物理地址。

## 1.3其他的虚拟化解决方案简介

### 1.3.1、Xen

Xen在架构上是一个典型的Type 1 Hypervisor，与KVM形成鲜明对比，如图1-8所示。严格来说，它没有宿主机的概念，而是由Xen Hypervisor（VMM）完全管控硬件，但用户却看不见、摸不着它，只能通过特殊的0号虚拟机（Dom0），通过其中xl工具栈（toolstack）与Xen Hypervisor交互来管理其他普通虚拟机（DomU）。0号虚拟机是一个运行修改过的半虚拟化的内核的Linux虚拟机。从架构上，Xen的虚拟化方案既利用了Linux内核的IO部分（Dom0的内核），将Linux内核的CPU、内存管理等核心部分排除在外由自己接手（Xen Hypervisor），所以，一开始就受到了Linux内核开发人员的抵制，致使Linux内核作为Dom0对Xen的支持部分一直不能合入Linux内核社区。一直到2010年，在采用基于内核的PVOPs方式大量重写了Xen代码以后，才勉强合入Linux内核社区。2011年，从Linux内核2.6.37版本开始，正式支持Xen Dom0。![](.\kvm实践\图1-8　Xen的架构.jpg)

### 1.3.2.VMware Workstation

VMware Workstation是VMware最早的产品，也是最广为人知的产品，1999年发布。在刚开始的时候，还没有硬件虚拟化技术，所以它是采用二进制翻译的方式实现虚拟化的。但是由于它的二进制翻译技术独步当时，性能还很出色，尤其跟当时同类产品相比。可以说，是VMware Workstation奠定了VMware在虚拟化软件行业的地位。VMwareWorkstation是桌面级虚拟化产品，运行在Windows、Linux和Mac操作系统上，是Type 2Hypervisor。使用它需要购买License，但VMware同时提供了与Workstation功能类似，只是有所删减的Workstation Player，供大家非商业化地免费使用。

### 1.3.3　HyperV

HyperV在架构上与Xen类似，也是Type 1 Hypervisor。它有Partition的概念，有一个Parent Partition，类似于Xen Dom0，有管理硬件资源的权限；HyperV的Child Partion就类似于普通的客户机DomU。对Hypervisor的请求以及对客户机的管理都要通过ParentPartition，硬件的驱动也由Parent Partition来完成。客户机看到的都是虚拟出来的硬件资源，它们对其虚拟硬件资源的访问都会被重定向到Parent Partition，由它来完成实际的操作，这种重定向是通过VMBus连接Parent Partition的VSP（Virtualization Service Provider）和child partition的VSC（Virtualization Service Consumer）来完成的，而这个过程对客户机OS都是透明的。图1-9中，HyperV Hypervisor运行在Ring-1，也就是Intel VMX技术的rootmode（特权模式），而parent partition和child partition的内核都运行在non-root mode的Ring0和Ring 3，也就是非特权模式的内核态和用户态。这样的架构安全性是比较好的。性能上如1.3.3节提到的那样，据微软自己说是略好于KVM的。

# 第2章　KVM原理简介

## 2.1　硬件虚拟化技术

### 2.1.1　CPU虚拟化

在没有CPU硬件虚拟化技术之前，通常使用指令的二进制翻译（binary translation）来实现虚拟客户机中CPU指令的执行，很早期的VMware就使用这样的方案，其指令执行的翻译比较复杂，效率比较低。所以Intel最早发布的虚拟化技术就是CPU虚拟化方面的，这才为KVM的出现创造了必要的硬件条件。

**Intel在处理器级别提供了对虚拟化技术的支持，被称为VMX**（virtual-machine extensions）。有两种VMX操作模式：**VMX根操作（root operation）与VMX非根操作（non-root operation）**。作为虚拟机监控器中的KVM就是运行在根操作模式下，而虚拟机客户机的整个软件栈（包括操作系统和应用程序）则运行在非根操作模式下。**进入VMX非根操作模式被称为“VM Entry”；从非根操作模式退出，被称为“VM Exit”。**

VMX的根操作模式与非VMX模式下最初的处理器执行模式基本一样，只是它现在支持了新的VMX相关的指令集以及一些对相关控制寄存器的操作。VMX的非根操作模式是一个相对受限的执行环境，为了适应虚拟化而专门做了一定的修改；在客户机中执行的一些特殊的敏感指令或者一些异常会触发“VM Exit”退到虚拟机监控器中，从而运行在VMX根模式。正是这样的限制，让虚拟机监控器保持了对处理器资源的控制。

一个虚拟机监控器软件的最基础的运行生命周期及其与客户机的交互如图2-1所示。![](.\kvm实践\图2-1　VMM与Guest之间的交互.jpg)

软件通过执行VMXON指令进入VMX操作模式下；在VMX模式下通过VMLAUNCH和VMRESUME指令进入客户机执行模式，即**VMX非根模式**；当在非根模式下触发VMExit时，处理器执行控制权再次回到宿主机的虚拟机监控器上；最后虚拟机监控可以执行VMXOFF指令退出VMX执行模式。

**逻辑处理器在根模式和非根模式之间的切换通过一个叫作VMCS（virtual-machinecontrol data structure）的数据结构来控制**；而VMCS的访问是通过VMCS指针来操作的。**VMCS指针是一个指向VMCS结构的64位的地址**，使用VMPTRST和VMPTRLD指令对VMCS指针进行读写，使用MREAD、VMWRITE和VMCLEAR等指令对VMCS实现配置。对于一个逻辑处理器，它可以维护多个VMCS数据结构，但是在任何时刻只有一个VMCS在当前真正生效。多个VMCS之间也是可以相互切换的，VMPTRLD指令就让某个VMCS在当前生效，而其他VMCS就自然成为不是当前生效的。一个虚拟机监控器会为一个虚拟客户机上的每一个逻辑处理器维护一个VMCS数据结构。

对于一个逻辑处理器，它可以维护多个VMCS数据结构，但是在任何时刻只有一个VMCS在当前真正生效, 多个VMCS之间也是可以相互切换的，VMPTRLD指令就让某个VMCS在当前生效.

**导致“VM Exit”的敏感指令**

1）一定会导致VM Exit的指令：CPUID、GETSEC、INVD、XSETBV等，以及VMX模式引入的INVEPT、INVVPID、VMCALL、VMCLEAR、VMLAUNCH、VMPTRLD、VMPTRST、VMRESUME、VMXOFF、VMXON等。
2）在一定的设置条件下会导致VM Exit的指令[1]：CLTS、HLT、IN、OUT、INVLPG、INVPCID、LGDT、LMSW、MONITOR、MOV from CR3、MOV to CR3、MWAIT、MWAIT、RDMSR、RWMSR、VMREAD、VMWRITE、RDRAND、RDTSC、XSAVES、XRSTORS等。如在处理器的虚拟机执行控制寄存器中的“HLT exiting”比特位被置为1时，HLT的执行就会导致VM Exit。
3）可能会导致VM Exit的事件：一些异常、三次故障（Triple fault）、外部中断、不可屏蔽中断（NMI）、INIT信号、系统管理中断（SMI）等。如在虚拟机执行控制寄存器中的“NMI exiting”比特位被置为1时，不可屏蔽中断就会导致VM Exit。

最后提一下，由于发生一次VM Exit的代价是比较高的（可能会消耗成百上千个CPU执行周期，而平时很多指令是几个CPU执行周期就能完成），所以对于VM Exit的分析是虚拟化中性能分析和调优的一个关键点。

### 2.1.2　内存虚拟化

​	内存虚拟化的目的是给虚拟客户机操作系统提供一个从0地址开始的连续物理内存空间，同时在多个客户机之间实现隔离和调度。在虚拟化环境中，内存地址的访问会主要涉及以下4个基础概念，图2-2形象地展示了虚拟化环境中内存地址。![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图2-2　虚拟化环境下的内存地址.jpg)

**1）客户机虚拟地址，GVA（Guest Virtual Address）**
**2）客户机物理地址，GPA（Guest Physical Address）**
**3）宿主机虚拟地址，HVA（Host Virtual Address）**
**4）宿主机物理地址，HPA（Host Physical Address）**

**内存虚拟化就是要将客户机虚拟地址（GVA）转化为最终能够访问的宿主机上的物理地址（HPA）。**对于客户机操作系统而言，它不感知内存虚拟化的存在，在程序访问客户机中虚拟地址时，通过CR3寄存器可以将其转化为物理地址，但是在虚拟化环境中这个物理地址只是客户机的物理地址，还不是真实内存硬件上的物理地址。所以，**虚拟机监控器就需要维护从客户机虚拟地址到宿主机物理地址之间的一个映射关系，在没有硬件提供的内存虚拟化之前，这个维护映射关系的页表叫作影子页表（Shadow Page Table）**。内存的访问和更新通常是非常频繁的，要维护影子页表中对应关系会非常复杂，开销也较大。同时需要为每一个客户机都维护一份影子页表，当客户机数量较多时，其影子页表占用的内存较大也会是一个问题。

**Intel CPU在硬件设计上就引入了EPT（Extended Page Tables，扩展页表），从而将客户机虚拟地址到宿主机物理地址的转换通过硬件来实现。**当然，这个转换是通过两个步骤来实现的，如图2-3所示。![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图2-3　基于EPT的内存地址转换.jpg)

首先，通过客户机CR3寄存器将客户机虚拟地址转化为客户机物理地址，
然后，通过查询EPT来实现客户机物理地址到宿主机物理地址的转化。
EPT的控制权在虚拟机监控器中，只有当CPU工作在非根模式时才参与内存地址的转换。使用EPT后，客户机在读写CR3和执行INVLPG指令时不会导致VM Exit，而且客户页表结构自身导致的页故障也不会导致VM Exit。所以通过引入硬件上EPT的支持，简化了内存虚拟化的实现复杂度，同时也提高了内存地址转换的效率。

### 2.1.3、I/O虚拟化

在虚拟化的架构下，虚拟机监控器必须支持来自客户机的I/O请求。通常情况下有以下4种I/O虚拟化方式。

1）设备模拟：在虚拟机监控器中模拟一个传统的I/O设备的特性，比如在QEMU中模拟一个Intel的千兆网卡或者一个IDE硬盘驱动器，在客户机中就暴露为对应的硬件设备。客户机中的I/O请求都由虚拟机监控器捕获并模拟执行后返回给客户机。
2）前后端驱动接口：在虚拟机监控器与客户机之间定义一种全新的适合于虚拟化环境的交互接口，比如常见的virtio协议就是在客户机中暴露为virtio-net、virtio-blk等网络和磁盘设备，在QEMU中实现相应的virtio后端驱动。
3）设备直接分配：将一个物理设备，如一个网卡或硬盘驱动器直接分配给客户机使用，这种情况下I/O请求的链路中很少需要或基本不需要虚拟机监控器的参与，所以性能很好。
4）设备共享分配：其实是设备直接分配方式的一个扩展。在这种模式下，一个（具有特定特性的）物理设备可以支持多个虚拟机功能接口，可以将虚拟功能接口独立地分配给不同的客户机使用。如SR-IOV就是这种方式的一个标准协议。

4种I/O虚拟化方式的优缺点表2-1　常见I/O虚拟化方式的优缺点![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\表2-1常见IO虚拟化方式的优缺点.jpg)

在这4种方式中，前两种都是纯软件的实现，后两种都需要特定硬件特性的支持。

设备直接分配在Intel平台上就是VT-d（Virtualization Technology For Directed I/O）特
性，一般在系统BIOS中可以看到相关的参数设置。Intel VT-d为虚拟机监控器提供了几个
重要的能力：I/O设备分配、DMA重定向、中断重定向、中断投递等。图

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图2-5　使用VT-d与传统设备完全模拟的虚拟化架构对比.jpg)

尽管VT-d特性支持的设备直接分配方式性能可以接近物理设备在非虚拟化环境中的性能极限，但是它有一个缺点：单个设备只能分配给一个客户机，而在虚拟化环境下一个宿主机上往往运行着多个客户机，很难保证每个客户机都能得到一个直接分配的设备。为了克服这个缺点，设备共享分配硬件技术就应运而生，其中SR-IOV（Single Root I/OVirtualization and Sharing）就是这样的一个标准。实现了SR-IOV规范的设备，有一个功能完整的PCI-e设备成为物理功能（Physical Function，PF）。在使能了SR-IOV之后，PF就会派生出若干个虚拟功能（Virtual Function，VF）。VF看起来依然是一个PCI-e设备，它拥有最小化的资源配置，有用独立的资源，可以作为独立的设备直接分配给客户机使用。Intel的很多高级网卡如82599系列网卡就支持SR-IOV特性，一个85299网卡PF就即可配置出多达63个VF，基本可满足单个宿主机上的客户机分配使用。当然，SR-IOV这种特性可以看作VT-d的一个特殊例子，所以SR-IOV除了设备本身要支持该特性，同时也需要硬件平台打开VT-d特性支持。图2-6展示了一个Intel以太网卡支持SR-IOV的硬件基础架构。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图2-6　支持SR-IOV的Intel网卡架构图.jpg)

## 2.2　KVM架构概述

KVM虚拟化的核心主要由以下两个模块组成：
1）KVM内核模块，它属于标准Linux内核的一部分，是一个专门提供虚拟化功能的模块，主要负责CPU和内存的虚拟化，包括：客户机的创建、虚拟内存的分配、CPU执行模式的切换、vCPU寄存器的访问、vCPU的执行。

2）QEMU用户态工具，它是一个普通的Linux进程，为客户机提供设备模拟的功能，包括模拟BIOS、PCI/PCIE总线、磁盘、网卡、显卡、声卡、键盘、鼠标等。同时它通过ioctl系统调用与内核态的KVM模块进行交互。

KVM是在硬件虚拟化支持下的完全虚拟化技术，所以它能支持在相应硬件上能运行的几乎所有的操作系统，如：Linux、Windows、FreeBSD、MacOS等。KVM的基础架构如图2-8所示。在KVM虚拟化架构下，每个客户机就是一个QEMU进程，在一个宿主机上有多少个虚拟机就会有多少个QEMU进程；客户机中的每一个虚拟CPU对应QEMU进程中的一个执行线程；一个宿主机中只有一个KVM内核模块，所有客户机都与这个内核模块进行交互。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图2-8　KVM虚拟化基础架构.jpg)



## 2.3　KVM内核模块

KVM内核模块是标准Linux内核的一部分，由于KVM的存在让Linux本身就变成了一个Hypervisor，可以原生地支持虚拟化功能。

KVM模块是KVM虚拟化的核心模块，它在内核中由两部分组成：一个是处理器架构无关的部分，用lsmod命令中可以看到，叫作kvm模块；另一个是处理器架构相关的部分，在Intel平台上就是kvm_intel这个内核模块。KVM的主要功能是初始化CPU硬件，打开虚拟化模式，然后将虚拟客户机运行在虚拟机模式下，并对虚拟客户机的运行提供一定的支持。

KVM仅支持硬件辅助的虚拟化，所以打开并初始化系统硬件以支持虚拟机的运行，是KVM模块的职责所在。以KVM在Intel公司的CPU上运行为例，在被内核加载的时候，KVM模块会先初始化内部的数据结构；做好准备之后，KVM模块检测系统当前的CPU，然后打开CPU控制寄存器CR4中的虚拟化模式开关，并通过执行VMXON指令将宿主操作系统（包括KVM模块本身）置于CPU执行模式的虚拟化模式中的根模式；最后，KVM模块创建特殊设备文件/dev/kvm并等待来自用户空间的命令。接下来，虚拟机的创建和运行将是一个用户空间的应用程序（QEMU）和KVM模块相互配合的过程。

/dev/kvm这个设备可以被当作一个标准的字符设备，KVM模块与用户空间QEMU的通信接口主要是一系列针对这个特殊设备文件的loctl调用。当然，每个虚拟客户机针对/dev/kvm文件的最重要的loctl调用就是“创建虚拟机”。在这里，“创建虚拟机”可以理解成KVM为了某个特定的虚拟客户机（用户空间程序创建并初始化）创建对应的内核数据结构。同时，KVM还会返回一个文件句柄来代表所创建的虚拟机。针对该文件句柄的loctl调用可以对虚拟机做相应的管理，比如创建用户空间虚拟地址和客户机物理地址及真实内存物理地址的映射关系，再比如创建多个可供运行的虚拟处理器（vCPU）。同样，KVM模块会为每一个创建出来的虚拟处理器生成对应的文件句柄，对虚拟处理器相应的文件句柄进行相应的loctl调用，就可以对虚拟处理器进行管理。

针对虚拟处理器的最重要的loctl调用就是“执行虚拟处理器”。通过它，用户空间准备好的虚拟机在KVM模块的支持下，被置于虚拟化模式中的非根模式下，开始执行二进制指令。在非根模式下，所有敏感的二进制指令都会被处理器捕捉到，处理器在保存现场之后自动切换到根模式，由KVM决定如何进一步处理（要么由KVM模块直接处理，要么返回用户空间交由用户空间程序处理）。

除了处理器的虚拟化，内存虚拟化也是由KVM模块实现的，包括前面提到的使用硬件提供的EPT特性，通过两级转换实现客户机虚拟地址到宿主机物理地址之间的转换。处理器对设备的访问主要是通过I/O指令和MMIO，其中I/O指令会被处理器直接截获，MMIO会通过配置内存虚拟化来捕捉。但是，外设的模拟一般不由KVM模块负责。

一般来说，只有对性能要求比较高的虚拟设备才会由KVM内核模块来直接负责，比如虚拟中断控制器和虚拟时钟，这样可以大量减少处理器模式切换的开销。而大部分的输入输出设备交给下一节将要介绍的用户态程序QEMU来负责。

2.4　QEMU用户态设备模拟
QEMU原本就是一个著名的开源虚拟机软件项目，而不是KVM虚拟化软件的一部分。与KVM不同，QEMU最初实现的虚拟机是一个纯软件的实现，通过二进制翻译来实现虚拟化客户机中的CPU指令模拟，所以性能比较低。但是，其优点是跨平台，QEMU支持在Linux、Windows、FreeBSD、Solaris、MacOS等多种操作系统上运行，能支持在QEMU本身编译运行的平台上就实现虚拟机的功能，甚至可以支持客户机与宿主机并不是同一个架构（比如在x86平台上运行ARM客户机）。作为一个存在已久的虚拟机监控器软件，QEMU的代码中有完整的虚拟机实现，包括处理器虚拟化、内存虚拟化，以及KVM也会用到的虚拟设备模拟（比如网卡、显卡、存储控制器和硬盘等）。

除了二进制翻译的方式，QEMU也能与基于硬件虚拟化的Xen、KVM结合，为它们提供客户机的设备模拟。通过与KVM的密切结合，让虚拟化的性能提升得非常高，在真实的企业级虚拟化场景中发挥重要作用，所以我们通常提及KVM虚拟化时就会说“QEMU/KVM”这样的软件栈。

最早期的KVM开发者们为了简化软件架构和代码重用，根据KVM特性在QEMU的基础上进行了修改（当然这部分修改已经合并回QEMU的主干代码，故现在的QEMU已原生支持KVM虚拟化特性）。从图2-8可以看出，每一个虚拟客户机在宿主机中就体现为一个QEMU进程，而客户机的每一个虚拟CPU就是一个QEMU线程。虚拟机运行期间，QEMU会通过KVM模块提供的系统调用进入内核，由KVM模块负责将虚拟机置于处理器的特殊模式下运行。遇到虚拟机进行I/O操作时，KVM模块会从上次的系统调用出口处返回QEMU，由QEMU来负责解析和模拟这些设备。

从QEMU角度来看，也可以说QEMU使用了KVM模块的虚拟化功能，为自己的虚拟机提供硬件虚拟化的加速，从而极大地提高了虚拟机的性能。除此之外，虚拟机的配置和创建，虚拟机运行依赖的虚拟设备，虚拟机运行时的用户操作环境和交互，以及一些针对虚拟机的特殊技术（如：动态迁移），都是由QEMU自己实现的。

QEMU除了提供完全模拟的设备（如：e1000网卡、IDE磁盘等）以外，还支持virtio协议的设备模拟。virtio是一个沟通客户机前端设备与宿主机上设备后端模拟的比较高性能的协议，在前端客户机中需要安装相应的virtio-blk、virtio-scsi、virtio-net等驱动，而QEMU就实现了virtio的虚拟化后端。QEMU还提供了叫作virtio-blk-data-plane的一种高性能的块设备I/O方式，它最初在QEMU 1.4版本中被引入。virtio-blk-data-plane与传统virtioblk
相比，它为每个块设备单独分配一个线程用于I/O处理，data-plane线程不需要与原QEMU执行线程同步和竞争锁，而且它使用ioeventfd/irqfd机制，同时利用宿主机Linux上的AIO（异步I/O）来处理客户机的I/O请求，使得块设备I/O效率进一步提高。

总之，QEMU既是一个功能完整的虚拟机监控器，也在QEMU/KVM的软件栈中承担设备模拟的工作。

## 2.5　与QEMU/KVM结合的组件

1.vhost-net
vhost-net是Linux内核中的一个模块，它用于替代QEMU中的virtio-net用户态的virtio网络的后端实现。使用vhost-net时，还支持网卡的多队列，整体来说会让网络性能得到较大提高。在6.1.6节中对vhost-net有更多的介绍。
2.Open vSwitch
Open vSwitch是一个高质量的、多层虚拟交换机，使用开源Apache2.0许可协议，主要用可移植性强的C语言编写的。它的目的是让大规模网络自动化可以通过编程扩展，同时仍然支持标准的管理接口和协议（例如NetFlow、sFlow、SPAN、RSPAN、CLI、LACP、802.1ag）。同时也提供了对OpenFlow协议的支持，用户可以使用任何支持OpenFlow协议的控制器对OVS进行远程管理控制。Open vSwitch被设计为支持跨越多个物理服务器的分
布式环境，类似于VMware的vNetwork分布式vswitch或Cisco Nexus 1000 V。Open vSwitch支持多种虚拟化技术，包括Xen/XenServer、KVM和VirtualBox。在KVM虚拟化中，要实现软件定义网络（SDN），那么Open vSwitch是一个非常好的开源选择。

3.DPDK
DPDK全称是Data Plane Development Kit，最初是由Intel公司维护的数据平面开发工具集，为Intel x86处理器架构下用户空间高效的数据包处理提供库函数和驱动的支持，现在也是一个完全独立的开源项目，它还支持POWER和ARM处理器架构。不同于Linux系统以通用性设计为目的，它专注于网络应用中数据包的高性能处理。具体体现在DPDK应用程序是运行在用户空间上，利用自身提供的数据平面库来收发数据包，绕过了Linux内核协议栈对数据包处理过程。其优点是：性能高、用户态开发、出故障后易恢复。在KVM架构中，为了达到非常高的网络处理能力（特别是小包处理能力），可以选择DPDK与QEMU中的vhost-user结合起来使用。
4.SPDK
SPDK全称是Storage Performance Development Kit，它可为编写高性能、可扩展的、用户模式的存储程序提供一系列工具及开发库。它与DPDK非常类似，其主要特点是：将驱动放到用户态从而实现零拷贝、用轮询模式替代传统的中断模式、在所有的I/O链路上实现无锁设计，这些设计会使其性能比较高。在KVM中需要非常高的存储I/O性能时，可以将QEMU与SPDK结合使用。
5.Ceph

Ceph是Linux上一个著名的分布式存储系统，能够在维护POSIX兼容性的同时加入复制和容错功能。Ceph由储存管理器（Object storage cluster对象存储集群，即OSD守护进程）、集群监视器（Ceph Monitor）和元数据服务器（Metadata server cluster，MDS）构成。其中，元数据服务器MDS仅仅在客户端通过文件系统方式使用Ceph时才需要。当客户端通过块设备或对象存储使用Ceph时，可以没有MDS。Ceph支持3种调用接口：对象存储，块存储，文件系统挂载。在libvirt和QEMU中都有Ceph的接口，所以Ceph与KVM虚拟化集成是非常容易的。在OpenStack的云平台解决方案中，Ceph是一个非常常用的存储后端。
6.libguestfs
libguestfs是用于访问和修改虚拟机的磁盘镜像的一组工具集合。libguestfs提供了访问和编辑客户机中的文件、脚本化修改客户机中的信息、监控磁盘使用和空闲的统计信息、P2V、V2V、创建客户机、克隆客户机、备份磁盘内容、格式化磁盘、调整磁盘大小等非常丰富的功能。libguestfs还提供了共享库，可以在C/C++、Python等编程语言中对其进行调用。libguestfs不需要启动KVM客户机就可以对磁盘镜像进行管理，功能强大且非常灵活，是管理KVM磁盘镜像的首选工具。

## 2.6　KVM上层管理工具

1.libvirt
libvirt是使用最广泛的对KVM虚拟化进行管理的工具和应用程序接口，已经是事实上的虚拟化接口标准，本节后部分介绍的其他工具都是基于libvirt的API来实现的。作为通用的虚拟化API，libvirt不但能管理KVM，还能管理VMware、Hyper-V、Xen、VirtualBox等其他虚拟化方案。
2.virsh
virsh是一个常用的管理KVM虚拟化的命令行工具，对于系统管理员在单个宿主机上进行运维操作，virsh命令行可能是最佳选择。virsh是用C语言编写的一个使用libvirt API的虚拟化管理工具，其源代码也是在libvirt这个开源项目中的。
3.virt-manager
virt-manager是专门针对虚拟机的图形化管理软件，底层与虚拟化交互的部分仍然是调用libvirt API来操作的。virt-manager除了提供虚拟机生命周期（包括：创建、启动、停止、打快照、动态迁移等）管理的基本功能，还提供性能和资源使用率的监控，同时内置了VNC和SPICE客户端，方便图形化连接到虚拟客户机中。virt-manager在RHEL、CentOS、Fedora等操作系统上是非常流行的虚拟化管理软件，在管理的机器数量规模较小时，virt-manager是很好的选择。因其图形化操作的易用性，成为新手入门学习虚拟化操作的首选管理软件。
4.OpenStack
OpenStack是一个开源的基础架构即服务（IaaS）云计算管理平台，可用于构建共有云和私有云服务的基础设施。OpenStack是目前业界使用最广泛的功能最强大的云管理平台，它不仅提供了管理虚拟机的丰富功能，还有非常多其他重要管理功能，如：对象存储、块存储、网络、镜像、身份验证、编排服务、控制面板等。OpenStack仍然使用libvirt

# 第3章　构建KVM环境

## 3.1　硬件系统的配置，在BIOS中开启VT和VT-d

​	在BIOS中，VT的选项通过“Advanced→Processor Configuration”来查看和设置，它的标识通常为“Intel(R)Virtualization Technology”或“Intel VT”等类似的文字说明。除了支持必需的处理器虚拟化扩展以外，如果服务器芯片还支持VT-d（VirtualizationTechnology for Directed I/O），建议在BIOS中将其打开，因为后面一些相对高级的设备的直接分配功能会需要硬件VT-d技术的支持。VT-d是对设备I/O的虚拟化硬件支持，在BIOS中的位置可能为“Advanced→Processor Configuration”或“Advanced→SystemAgent(SA)Configuration”，它在BIOS中的标志一般为“Intel(R)VT for Directed I/O”或“IntelVT-d”。

1）BIOS中的Advanced选项，如图3-1所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-1　BIOS中的Advanced选项.jpg)

2）BIOS中Enabled的VT和VT-d选项，如图3-2所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-2　BIOS中Enabled的VT和VT-d选项.jpg)

通过检查/proc/cpuinfo文件中的CPU特性标志（flags）来查看CPU目前是否支持硬件虚拟化。在x86和x86-64平台中，Intel系列CPU支持虚拟化的标志为“vmx”，AMD系列CPU的标志为“svm”。所以可以用以下命令行查看“vmx”或者“svm”标志：

`[root@kvm-host ~]# grep -E "svm|vmx" /proc/cpuinfo`
`flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse <!-– 此处省略多行其余CPU或core的flags输出信息 -->`

## 3.2　安装宿主机Linux系统

在选择哪些安装包（SOFTWARE SELECTION）时（图3-3），点进去选择“Serverwith GUI”[2]，而不是默认的“Minimal Install”，如图3-4所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\3-3.jpg)

在选择了“Server with GUI”之后，右侧还有可以额外增加的组件供选择（见图3-4），我们需要选上“Development Tools”，因为在本书的KVM编译过程中以及其他实验中可能会用到，其中包括一些比较重要的软件包，比如：cc、git、make等（一般被默认选中）![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\3-4.jpg)

然后，单击“Done”按钮并继续进行后面的安装流程。可以安装相应的软件包，安装过程的一个快照如图3-5所示。

## 3.3　编译和安装KVM——内核空间KVM模块

下载KVM源代码，配置KVM(配置命令），编译KVM，安装KVM

### 3.3.1　下载KVM源代码

下载最新KVM源代码，主要有以下3种方式：
1）下载KVM项目开发中的代码仓库kvm.git。
2）下载Linux内核的代码仓库linux.git。
3）打包下载Linux内核的源代码（Tarball[1]格式）。

#### 1.下载kvm.git

kvm.git的下载链接有以下3个URL，可用于下载最新的KVM的开发代码仓库。
git://git.kernel.org/pub/scm/virt/kvm/kvm.git
http://git.kernel.org/pub/scm/virt/kvm/kvm.git
https://git.kernel.org/pub/scm/virt/kvm/kvm.git

**kvm.git的下载方式和过程为以下命令行所示：**

`[root@kvm-host ~]# git clone`
`git://git.kernel.org/pub/scm/virt/kvm/kvm.git`
`Cloning into 'kvm'...`
`remote: Counting objects: 5017872, done.`
`remote: Compressing objects: 100% (938249/938249), done.`
`Receiving objects: 100% (5017872/5017872), 1006.69 MiB | 60.72 MiB/s, done.`
`remote: Total 5017872 (delta 4229078), reused 4826094 (delta 4038351)`
`Resolving deltas: 100% (4229078/4229078), done.`
`Checking out files: 100% (55914/55914), done.`
`[root@kvm-host ~]# cd kvm/`
`[root@kvm-host kvm]# pwd`
`/root/kvm`

#### 2.下载linux.git

在内核源码的网页http://git.kernel.org/?p=linux/kernel/git/torvalds/linux.git中可以看到，其源码仓库也有以下
3个链接可用：
git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
http://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
这3个URL中源码内容是完全相同的，可以使用git clone命令复制到本地，其具体操作方式与前一种（kvm.git）的下载方式完全一样。

#### 3.下载Linux的Tarball

在Linux官方网站（http://kernel.org）上，也提供Linux内核的Tarball文件下载。除了在其首页上单击一些Tarball之外，也可以到以下网址下载Linux内核的各个版本的Tarball：
·ftp://ftp.kernel.org/pub/linux/kernel。
·http://www.kernel.org/pub/linux/kernel。
kernel.org还提供一种rsync的方式下载，此处不详细叙述，请参见其官网首页的提示。
以用wget下载linux-4.8.1.tar.xz为例，命令行代码如下：

`[root@kvm-host ~]# wget`
`https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.8.1.tar.xz`
`<!-此处省略输出->`

#### 4.通过kernel.org的镜像站点下载

·清华大学开源镜像站：http://mirror.tuna.tsinghua.edu.cn，其中的链接地址https://mirror.tuna.tsinghua.edu.cn/kernel与http://www.kernel.org/pub/linux/kernel是同步的，用起来比较方便。
·北京交通大学的一个开源镜像站：http://mirror.bjtu.edu.cn/kernel/linux/kernel。
还有以下两个镜像站推荐给大家：
·网易开源镜像站，http://mirrors.163.com。
·搜狐开源镜像站，http://mirrors.sohu.com。

### 3.3.2　配置KVM

在kvm.git（Linux kernel）代码目录下，运行“make help”命令可以得到一些关于如何配置和编译kernel的帮助手册。命令行如下：
`[root@kvm-host kvm]# make help`
`Cleaning targets:`
`clean - Remove most generated files but keep the config and enough`
`build support to build external modules`
`mrproper - Remove all generated files + config + various backup files`
`distclean - mrproper + remove editor backup and patch files`
`Configuration targets:`
`config - Update current config utilising a line-oriented program`
`nconfig - Update current config utilising a ncurses menu based program`
`menuconfig - Update current config utilising a menu based program`
`xconfig - Update current config utilising a Qt based front-end`
`gconfig - Update current config utilising a GTK+ based front-end`
`oldconfig - Update current config utilising a provided .config as base`
`localmodconfig - Update current config disabling modules not loaded`
`localyesconfig - Update current config converting local mods to core`
`silentoldconfig - Same as oldconfig, but quietly, additionally update deps`
`defconfig - New config with default from ARCH supplied defconfig`
`savedefconfig - Save current config as ./defconfig (minimal config)`
`allnoconfig - New config where all options are answered with no`
`allyesconfig - New config where all options are accepted with yes`
`allmodconfig - New config selecting modules when possible`
`alldefconfig - New config with all symbols set to default`
`randconfig - New config with random answer to all options`
`listnewconfig - List new options`
`olddefconfig - Same as silentoldconfig but sets new symbols to their default`
`value`
`kvmconfig - Enable additional options for kvm guest kernel support`
`xenconfig - Enable additional options for xen dom0 and guest kernel support`
`tinyconfig - Configure the tiniest possible kernel`
`<!- 此处省略数十行帮助信息 ->`
对KVM或Linux内核配置时常用的一些配置命令解释如下。
1）make config：基于文本的最为传统也是最为枯燥的一种配置方式，但是它可以适用于任何情况之下。这种方式会为每一个内核支持的特性向用户提问，如果用户回答“y”，则把特性编译进内核；回答“m”，则把特性作为模块进行编译；回答“n”，则表示不对该特性提供支持；输入“？”则显示该选项的帮助信息。在了解之后再决定处理该选项的方式。在回答每个问题前必须考虑清楚，如果在配置过程中因为失误而给了错误的回答，就只能按“Ctrl+c”组合键强行退出然后重新配置了。

2）make oldconfig：make oldconfig和make config类似，但是它的作用是在现有的内核设置文件基础上建立一个新的设置文件，只会向用户提供有关新内核特性的问题。在新内核升级的过程中，make oldconfig非常有用，用户将现有的配置文件.config复制到新内核的源码中，执行make oldconfig，此时，用户只需要回答那些针对新增特性的问题。

3）make silentoldconfig：和上面make oldconfig一样，只是额外悄悄地更新选项的依赖关系。

4）make olddefconfig：和上面make silentoldconfig一样，但不需要手动交互，而是对新选项以其默认值配置。

5）make menuconfig：基于终端的一种配置方式，提供了文本模式的图形用户界面，用户可以通过移动光标来浏览所支持的各种特性。使用这种配置方式时，系统中必须安装ncurses库，否则会显示“Unable to find the ncurses libraries”的错误提示。其中“Y”“N”“M”“？”输入键的选择功能与前面make config中介绍的一致。

6）make xconfig：基于X Window的一种配置方式，提供了漂亮的配置窗口，不过只能在X Server上运行X桌面应用程序时使用。它依赖于QT，如果系统中没有安装QT库，则会出现“Unable to find any QT installation”的错误提示。

7）make gconfig：与make xconfig类似，不同的是make gconfig依赖于GTK库。

8）make defconfig：按照内核代码中提供的默认配置文件对内核进行配置（在Intelx86-64平台上，默认配置为arch/x86/configs/x86_64_defconfig），生成.config文件可以用作初始化配置，然后再使用make menuconfig进行定制化配置。

9）make allyesconfig：尽可能多地使用“y”输入设置内核选项值，生成的配置中包含了全部的内核特性。

10）make allnoconfig：除必需的选项外，其他选项一律不选（常用于嵌入式Linux系统的编译）。

11）make allmodconfig：尽可能多地使用“m”输入设置内核选项值来生成配置文件。

12）make localmodconfig：会执行lsmod命令查看当前系统中加载了哪些模块（Modules），并最终将原来的.config中不需要的模块去掉，仅保留前面lsmod命令查出来的那些模块，从而简化了内核的配置过程。这样做确实方便了很多，但是也有个缺点：该方法仅能使编译出的内核支持当前内核已经加载的模块。因为该方法使用的是lsmod查询得到的结果，如果有的模块当前没有被加载，那么就不会编到新的内核中。

下面以make menuconfig为例，介绍一下如何选择KVM相关的配置（系统中要安装好ncurses-devel包）。运行make menuconfig后显示的界面如图3-6所示。![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-6　make menuconfig命令的选择界面.jpg)

选择了Virtualization之后，进入其中进行详细配置，包括选中KVM、选中对处理器的支持（比如：KVM for Intel processors support，KVM for AMD processors support）等，如图3-7所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-7　Virtualization中的配置选项.jpg)



提示：为了确保生成的.config文件生成的kernel是实际可以工作的（直接makedefconfig生成的.config文件编译出来的kernel常常是不能工作的），最佳实践是以你当前使用的config（比如，我们安装好RHEL 7.3的OS以后，/boot/config-3.10.0-xxx.x86_64）为基础，将它复制到你的linux目录下，重命名为.config，然后通过make olddefconfig更新补充一下这个.config。
在配置完成之后，就会在kvm.git目录下面生成一个.config文件。最好检查一下KVM相关的配置是否正确。在本次配置中，与KVM直接相关的几个配置项主要情况如下：

`CONFIG_HAVE_KVM=y`
`CONFIG_HAVE_KVM_IRQCHIP=y`
`CONFIG_HAVE_KVM_EVENTFD=y`
`CONFIG_KVM_APIC_ARCHITECTURE=y`
`CONFIG_KVM_MMIO=y`
`CONFIG_KVM_ASYNC_PF=y`
`CONFIG_HAVE_KVM_MSI=y`
`CONFIG_VIRTUALIZATION=y`
`CONFIG_KVM=m`
`CONFIG_KVM_INTEL=m`
`CONFIG_KVM_AMD is not set`
`CONFIG_KVM_MMU_AUDIT=y`

### 3.3.3　编译KVM

在对KVM源代码进行了配置之后，编译KVM就是一件比较容易的事情了。它的编译过程完全是一个普通Linux内核编译的过程，需要经过编译kernel、编译bzImage和编译module等3个步骤。编译bzImage这一步不是必需的，在本章示例中，config中使用了initramfs，所以这里需要这个bzImage，用于生成initramfs image。另外，在最新的Linuxkernel代码中，根据makefile中的定义可以看出，直接执行“make”或“make all”命令就可以将这里提及的3个步骤全部包括在内。本节是为了更好地展示编译的过程，才将编译的步骤分为这3步来解释。

1）编译kernel的命令为“make vmlinux”，其编译命令和输出如下：

`[root@kvm-host kvm]# make vmlinux -j 20`
`<!- 此处省略数千行编译时的输出信息 ->`
`LINK vmlinux`
`LD vmlinux.o`
`MODPOST vmlinux.o`
`GEN .version`
`CHK include/generated/compile.h`
`UPD include/generated/compile.h`
`CC init/version.o`
`LD init/built-in.o`
`KSYM .tmp_kallsyms1.o`
`KSYM .tmp_kallsyms2.o`
`LD vmlinux #这里就是编译、链接后生成了启动所需的Linux kernel文件`
`SORTEX vmlinux`
`SYSMAP System.map`

其中，编译命令中的“-j”参数并非必需的，它是让make工具用多任务（job）来编译。比如，上面命令中提到的“-j 20”，会让make工具最多创建20个GCC进程，同时来执行编译任务。在一个比较空闲的系统上，有一个推荐值作为-j参数的值，即大约为2倍于系统上的CPU的core的数量（CPU超线程也算core）。如果-j后面不跟数字，则make会根据现在系统中的CPU core的数量自动安排任务数（通常比core的数量略多一点）。
2）执行编译bzImage的命令“make bzImage”，其输出如下：

`[root@kvm-host kvm]# make bzImage`
`CHK include/config/kernel.release`
`CHK include/generated/uapi/linux/version.h`
`CHK include/generated/utsrelease.h`
`<!- 此处省略数十行编译时的输出信息 ->`
`LD arch/x86/boot/setup.elf`
`OBJCOPY arch/x86/boot/setup.bin`
`OBJCOPY arch/x86/boot/vmlinux.bin`
`HOSTCC arch/x86/boot/tools/build`
`BUILD arch/x86/boot/bzImage #这里生成了我们需要的bzImage文件`
`Setup is 17276 bytes (padded to 17408 bytes).`
`System is 5662 kB`
`CRC 3efff614`
`Kernel: arch/x86/boot/bzImage is ready (#2)`

3）编译kernel和bzImage之后编译内核的模块，命令为“make modules”，其命令行输出如下：

`[root@kvm-host kvm]# make modules -j 20`
`<!- 此处省略数千行编译时的输出信息 ->`
`IHEX2FW firmware/emi26/loader.fw`
`IHEX2FW firmware/emi26/firmware.fw`
`IHEX2FW firmware/emi26/bitstream.fw`
`IHEX2FW firmware/emi62/loader.fw`
`IHEX2FW firmware/emi62/bitstream.fw`
`IHEX2FW firmware/emi62/spdif.fw`
`IHEX2FW firmware/emi62/midi.fw`
`H16TOFW firmware/edgeport/boot2.fw`
`H16TOFW firmware/edgeport/boot.fw`
`H16TOFW firmware/edgeport/down.fw`
`H16TOFW firmware/edgeport/down2.fw`
`IHEX2FW firmware/whiteheat_loader.fw`
`IHEX2FW firmware/whiteheat.fw`
`IHEX2FW firmware/keyspan_pda/keyspan_pda.fw`
`IHEX2FW firmware/keyspan_pda/xircom_pgs.fw`

### 3.3.4　安装KVM

编译完KVM之后，下面介绍如何安装KVM。
KVM的安装包括两个步骤：安装module，安装kernel与initramfs。
**1.安装module**
通过“make modules_install”命令可以将编译好的module安装到相应的目录中，默认情况下module被安装到/lib/modules/$kernel_version/kernel目录中。

`[root@kvm-host kvm]# make modules_install`
`<!- 此处省略千余行安装时的输出信息 ->`
`INSTALL /lib/firmware/whiteheat.fw`
`INSTALL /lib/firmware/keyspan_pda/keyspan_pda.fw`
`INSTALL /lib/firmware/keyspan_pda/xircom_pgs.fw`
`DEPMOD 4.8.0+`
安装好module之后，可以查看一下相应的安装路径，可看到kvm模块也已经安装。如下所示：
`[root@kvm-host kvm]# ll /lib/modules/4.8.0+/kernel/`
`total 16`
`drwxr-xr-x 3 root root 16 Oct 15 15:05 arch`
`drwxr-xr-x 3 root root 4096 Oct 15 15:05 crypto`
`drwxr-xr-x 66 root root 4096 Oct 15 15:06 drivers`
`drwxr-xr-x 26 root root 4096 Oct 15 15:06 fs`
`drwxr-xr-x 3 root root 18 Oct 15 15:06 kernel`
`drwxr-xr-x 4 root root 152 Oct 15 15:06 lib`
`drwxr-xr-x 2 root root 31 Oct 15 15:06 mm`
`drwxr-xr-x 32 root root 4096 Oct 15 15:06 net`
`drwxr-xr-x 10 root root 135 Oct 15 15:06 sound`
`drwxr-xr-x 3 root root 16 Oct 15 15:06 virt`
`[root@kvm-host kvm]# ll /lib/modules/4.8.0+/kernel/arch/x86/kvm/`
`total 11256`
`-rw-r--r-- 1 root root 1940806 Oct 15 15:05 kvm-intel.ko`
`-rw-r--r-- 1 root root 9583878 Oct 15 15:05 kvm.ko`

**2.安装kernel和initramfs**

通过“make install”命令可以安装kernel和initramfs，命令行输出如下：
`[root@kvm-host kvm]# make install`
`sh ./arch/x86/boot/install.sh 4.8.0+ arch/x86/boot/bzImage \`
`System.map "/boot"`
`[root@kvm-host kvm]# ll /boot -t`
`......`
`drwx------. 6 root root 103 Oct 15 15:12 grub2`
`-rw-r--r-- 1 root root 58106303 Oct 15 15:11 initramfs-4.8.0+.img`
`lrwxrwxrwx 1 root root 23 Oct 15 15:10 System.map -> /boot/System.map-4.8.0+`
`lrwxrwxrwx 1 root root 20 Oct 15 15:10 vmlinuz -> /boot/vmlinuz-4.8.0+`
`-rw-r--r-- 1 root root 3430941 Oct 15 15:10 System.map-4.8.0+`
`-rw-r--r-- 1 root root 5815104 Oct 15 15:10 vmlinuz-4.8.0+`
可见，在/boot目录下生成了内核（vmlinuz）和initramfs等内核启动所需的文件。
在运行make install之后，在grub配置文件（如：/boot/grub2/grub.cfg）中也自动添加一个grub选项，如下所示：
`menuentry 'Redhat Enterprise Linux Server (4.8.0+) 7.2 (Maipo)' ... {`
`load_video`
`insmod gzio`
`insmod part_msdos`
`insmod xfs`
`set root='hd1,msdos1'`
`if [ x$feature_platform_search_hint = xy ]; then`
`search --no-floppy --fs-uuid --set=root --hint-bios=hd1,msdos1 --hint-efi=hd1, msdos1 --hint-baremetal=ahci1,else`
`search --no-floppy --fs-uuid --set=root da2e2d53-4b33-4bfe-a649-73fba55a7a9d`
`fi`
`linux16 /vmlinuz-4.8.0+ root=/dev/mapper/rhel-root ro rd.lvm.lv=rhel/root crashkernel=auto rd.lvm.lv=rhel/swap initrd16 /initramfs-4.8.0+.img`
}
检查了grub之后，重新启动系统，选择刚才为了KVM而编译、安装的内核启动。
系统启动后，登录进入系统，通常情况下，系统启动时默认已经加载了kvm和kvm_intel这两个模块。如果没有加载，手动用modprobe命令依次加载kvm和kvm_intel模块。
`[root@kvm-host kvm]# modprobe kvm`
`[root@kvm-host kvm]# modprobe kvm_intel`
`[root@kvm-host kvm]# lsmod | grep kvm`
`kvm_intel 192512 0`
`kvm 577536 1 kvm_intel`
确认KVM相关的模块加载成功后，检查/dev/kvm这个文件，它是kvm内核模块提供给用户空间的QEMU程序使用的一个控制接口，它提供了客户机（Guest）操作系统运行所需要的模拟和实际的硬件设备环境。
`[root@kvm-host kvm]# ls -l /dev/kvm`
`crw-rw-rw-+ 1 root kvm 10, 232 Oct 9 15:22 /dev/kvm`

## 3.4　编译和安装QEMU

除了在内核空间的KVM模块之外，在用户空间需要QEMU[1]来模拟所需要的CPU和设备模型，以及启动客户机进程，这样才有了一个完整的KVM运行环境。
在编译和安装了KVM并且启动到编译的内核之后，下面来看一下QEMU的编译和安装。
[1] 关于QEMU项目，可以参考其官方网站：http://wiki.qemu.org/Main_Page。

### 3.4.1　下载QEMU源代码

在并入主流QEMU以后，目前的QEMU项目针对KVM/x86的部分依然是由Redhat公司的Paolo Bonzini作为维护者（Maintainer），代码的git url托管在qemu-project.org上。
QEMU开发代码仓库的网页连接为：http://git.qemu.org/qemu.git。
其中，可以看到有如下2个URL链接可供下载开发中的最新qemu-kvm的代码仓库。
git://git.qemu.org/qemu.git
http://git.qemu.org/git/qemu.git
可以根据自己实际需要选择当中任一个，用git clone命令下载即可，它们是完全一样的。
另外，也可以到以下下载链接中根据需要下载最近几个发布版本的代码压缩包。
http://wiki.qemu.org/Download
在本节后面讲解编译时，是以下载开发中的最新的qemu.git为例的。获取其代码仓库过程如下：
`[root@kvm-host ~]# git clone git://git.qemu.org/qemu.git`
`Cloning into 'qemu'...`
`remote: Counting objects: 294725, done.`
`remote: Compressing objects: 100% (59425/59425), done.`
`remote: Total 294725 (delta 238595), reused 289874 (delta 234513)`
`Receiving objects: 100% (294725/294725), 94.23 MiB | 37.66 MiB/s, done.`
`Resolving deltas: 100% (238595/238595), done.`
`[root@kvm-host ~]# cd qemu`
`[root@kvm-host qemu]# ls`
`accel.c CODING_STYLE dtc kvm-all.c numa.c qemu-io.c README target-mips trace`
<!- 此处省略qemu文件夹下众多文件及子文件夹 ->

### 3.4.2　配置和编译QEMU

QEMU的配置并不复杂，通常情况下，直接运行代码仓库中configure文件进行配置即可。当然，如果对其配置不熟悉，可以运行“./configure--help”命令查看配置的一些选项及其帮助信息。
显示配置的帮助信息如下：
`[root@kvm-host qemu]# ./configure --help`
`Usage: configure [options]`
`Options: [defaults in brackets after descriptions]`
`Standard options:`
`--help print this message`
`--prefix=PREFIX install in PREFIX [/usr/local]`
`--interp-prefix=PREFIX where to find shared libraries, etc.`
`use %M for cpu name [/usr/gnemul/qemu-%M]`
`--target-list=LIST set target list (default: build everything)`
`Available targets: aarch64-softmmu alpha-softmmu`
`arm-softmmu cris-softmmu i386-softmmu lm32-softmmu`
`m68k-softmmu microblazeel-softmmu microblaze-softmmu`
`mips64el-softmmu mips64-softmmu mipsel-softmmu`
`mips-softmmu moxie-softmmu or32-softmmu`
`ppc64-softmmu ppcemb-softmmu ppc-softmmu`
`s390x-softmmu sh4eb-softmmu sh4-softmmu`
`sparc64-softmmu sparc-softmmu tricore-softmmu`
`unicore32-softmmu x86_64-softmmu xtensaeb-softmmu`
`xtensa-softmmu aarch64-linux-user alpha-linux-user`
`armeb-linux-user arm-linux-user cris-linux-user`
`i386-linux-user m68k-linux-user`
`microblazeel-linux-user microblaze-linux-user`
`mips64el-linux-user mips64-linux-user`
`mipsel-linux-user mips-linux-user`
`mipsn32el-linux-user mipsn32-linux-user`
`or32-linux-user ppc64abi32-linux-user`
`ppc64le-linux-user ppc64-linux-user ppc-linux-user`
`s390x-linux-user sh4eb-linux-user sh4-linux-user`
`sparc32plus-linux-user sparc64-linux-user`
`sparc-linux-user tilegx-linux-user`
`unicore32-linux-user x86_64-linux-user`
`Advanced options (experts only):`
`<!- 此处省略百余行帮助信息的输出 ->`
`NOTE: The object files are built at the place where configure is launched`
以上configure选项中我们特别提一下“--target-list”，它指定QEMU对客户机架构的支持。可以看到，对应的选项非常多，表面上QEMU对客户机的架构类型的支持是非常全面的。由于在本书中（也是多数的实际使用场景）我们只使用x86架构的客户机，因此指定“--target-list=x86_64-softmmu”，可以节省大量的编译时间。
执行configure文件进行配置的过程如下：
`[root@kvm-host qemu]# ./configure --target-list=x86_64-softmmu`
`Install prefix /usr/local`
`BIOS directory /usr/local/share/qemu`
`...`
`ELF interp prefix /usr/gnemul/qemu-%M`
`Source path /root/qemu`
`<!-- 以上是指定一些目录前缀，省略十几行。可以由configure的--prefix选项影响 -->`
`C compiler cc`
`Host C compiler cc`
`...`
`QEMU_CFLAGS -I/usr/include/pixman-1 -Werror -pthread -I/usr/include/glib-2.0 -I/usr/lib64/glib-2.0/include LDFLAGS -Wl,--warn-common -Wl,-z,relro -Wl,-z,now -pie -m64 -g`
`<!-- 以上显示了后续编译qemu时会采用的编译器及编译选项。也可以由configure对应选项控制。-->`
`...`
`host CPU x86_64`
`host big endian no`
`target list x86_64-softmmu #这里就是我们--target-list指定的`
`...`
`VNC support yes #通常需要通过VNC连接到客户机中。默认`
`...`
`KVM support yes #这是对KVM的支持。默认`
`...`
在配置完以后，qemu目录下会生成config-host.mak和config.status文件。confighost.mak里面可以查看你通过上述configure之后的结果，它会在后续make中被引用。config.status是为用户贴心设计的，便于后续要重新configure时，只要执行“./config.status”就可以恢复上一次configure的配置。这对你苦心配置了很多选项，而后
又忘了的情况非常有用。
经过配置之后，编译就很简单了，直接执行make即可。
最后，编译生成x86_64-softmmu/qemu-system-x86_64文件，就是我们需要的用户空间用于其KVM客户机的工具了（在多数Linux发行版中自带的qemu-kvm软件包的命令行是qemu-kvm，只是名字不同的downstream，用户可以等同视之）。

### 3.4.3　安装QEMU

编译完成之后，运行“make install”命令即可安装QEMU。

QEMU安装过程的主要任务有这几个：创建QEMU的一些目录，复制一些配置文件到相应的目录下，复制一些firmware文件（如：sgabios.bin、kvmvapic.bin）到目录下，以便qemu命令行启动时可以找到对应的固件供客户机使用；复制keymaps到相应的目录下，以便在客户机中支持各种所需键盘类型；复制qemu-system-x86_64、qemu-img等可执行程序到对应的目录下。下面的一些命令行检查了QEMU被安装之后的系统状态。

`[root@kvm-host qemu]# ls /usr/local/share/qemu/`
`acpi-dsdt.aml efi-eepro100.rom keymaps openbios-sparc32 pxe-e1000.rom`
`QEMU,cgthree.bin slof.bin vgabios-qxl.bin`
`bamboo.dtb efi-ne2k_pci.rom kvmvapic.bin openbios-sparc64`
`pxe-eepro100.rom qemu-icon.bmp spapr-rtas.bin`
`vgabios-stdvga.bin`
`bios-256k.bin efi-pcnet.rom linuxboot.bin palcode-clipper`
`pxe-ne2k_pci.rom qemu_logo_no_text.svg trace-events-all`
`vgabios-virtio.bin`
`bios.bin efi-rtl8139.rom linuxboot_dma.bin petalogix-ml605.dtb`
`pxe-pcnet.rom QEMU,tcx.bin u-boot.e500`
`vgabios-VMware.bin`
`efi-e1000e.rom efi-virtio.rom multiboot.bin petalogix-s3adsp1800.dtb`
`pxe-rtl8139.rom s390-ccw.img vgabios.bin`
`efi-e1000.rom efi-vmxnet3.rom openbios-ppc ppc_rom.bin`
`pxe-virtio.rom sgabios.bin vgabios-cirrus.bin`
`[root@kvm-host qemu]# ls /usr/local/share/qemu/keymaps/`
ar bepo common cz da de de-ch en-gb en-us es et fi fo fr fr-be fr-ca fr-ch hr hu is it ja 

由于QEMU是用户空间的程序，安装之后不用重启系统，直接用qemu-systemx86_64、qemu-img这样的命令行工具就可以了。

## 3.5　安装客户机

安装客户机（Guest）之前，我们需要创建一个镜像文件或者磁盘分区等，来存储客户机中的系统和文件。关于客户机镜像有很多种制作和存储方式（将在第4章中进行详细的介绍），本节只是为了快速地演示安装一个客户机，采用了本地创建一个镜像文件，然后将镜像文件作为客户机的硬盘，将客户机操作系统（以RHEL 7为例）安装在其中。

首先，需要创建一个镜像文件。我们使用上节中生成好的qemu-img工具来完成这个任务。它不仅用于创建guest，还可以在后续管理guest image。详见“qemu-img--help”及“man qemu-img”。

`[root@kvm-host ~]# qemu-img create -f raw rhel7.img 40G`
`Formatting 'rhel7.img', fmt=raw size=42949672960`
上述就是用qemu-img create命令创建了一个空白的guest image，以raw格式，image文件的名字是“rhel7.img”，大小是40G。虽然我们看到它的大小是40G，但是它并不占用任何磁盘空间。

`[root@kvm-host ~]# ls -lh rhel7.img`
`-rw-r--r-- 1 root root 40G Oct 15 10:44 rhel7.img`
`[root@kvm-host ~]# du -h rhel7.img`
`0 rhel7.img`

这是因为qemu-img聪明地为你按实际需求分配文件的实际大小，它将随着image实际的使用而增大。qemu-img也支持设置参数让你可以一开始就实际占有40G（当然建立的过程也就比较耗时，还会占用你更大空间。所以qemu-img默认的方式是按需分配的），如下：
`[root@kvm-host ~]# qemu-img create -f raw -o preallocation=full rhel7.img 40G`
`Formatting 'rhel7.img', fmt=raw size=42949672960 preallocation=full`
`[root@kvm-host ~]# ls -lh rhel7.img`
`-rw-r--r-- 1 root root 40G Oct 15 10:58 rhel7.img`
`[root@kvm-host ~]# du -h rhel7.img`
`40G rhel7.img`
除raw格式以外，qemu-img还支持创建其他格式的image文件，比如qcow2，甚至是其他虚拟机用到的文件格式，比如VMware的vmdk、vdi、vhd等。不同的文件格式会有不同的“-o”选项。

创建完空白guest image之后，我们将RHEL 7安装所需的ISO文件准备好。

`[root@kvm-host ~]# ls -l RHEL-7.2-20151030.0-Server-x86_64-dvd1.iso`
`-rw-r--r-- 1 root root 4043309056 Oct 30 2015 RHEL-7.2-20151030.0-Server-x86_64-dvd1.iso`

启动客户机，并在其中用准备好的ISO安装系统，命令行如下：

qemu-system-x86_64 -enable-kvm -m 8G -smp 4 -boot once=d -cdrom RHEL-7.2-20151030.0-Server-x86_64-dvd1.iso rhel7.

其中，-m 8G是给客户机分配8G内存，-smp 4是指定客户机为对称多处理器结构并分配4个CPU，-boot once=d是指定系统的启动顺序为首次光驱，以后再使用默认启动项（硬盘）[1]，-cdrom**是分配客户机的光驱。默认情况下，QEMU会启动一个VNC server端口（5900），可以用vncviwer工具[2]来连接到QEMU的VNC端口查看客户机。

通过启动时的提示，这里可以使用“vncviewer：5900”命令连接到QEMU启动的窗口。根据命令行指定的启动顺序，当有CDROM时，客户机默认会从光驱引导，启动后即可进入客户机系统安装界面，如图3-8所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-8　客户机安装的选择界面.jpg)

图3-8　客户机安装的选择界面可以选择Install安装客户机操作系统，和安装普通Linux系统类似，根据需要做磁盘分区、选择需要的软件包等。安装过程中的一个快照如图3-9所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-9　客户机安装过程的快照.jpg)

图3-9　客户机安装过程的快照

在系统安装完成后，客户机中安装程序提示信息，如图3-10所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-10　客户机安装完成后的提示信息.jpg)

图3-10　客户机安装完成后的提示信息



和普通的Linux系统安装一样，安装完成后，重启系统即可进入刚才安装的客户机操作系统。

[1] 这里这样选择是因为RHEL 7首次安装好以后需要从硬盘重启。
[2] 在宿主机中需要安装包含vncserver和vncviewer工具的软件包，如在RHEL 7系统中，可以安装tigervnc-server和tigervnc这两个RPM软件包。

## 3.6　启动第一个KVM客户机

在安装好了系统之后，就可以使用镜像文件来启动并登录到自己安装的系统之中了。通过如下的简单命令行即可启动一个KVM的客户机。

`[root@kvm-host ~]#qemu-system-x86_64 -m 8G -smp 4 /root/rhel7.img`
`VNC server running on ‘::1:5900’`
用vncviwer命令（此处命令为vncviwer：5900）查看客户机的启动情况。

客户机启动完成后的登录界面如图3-11所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图3-11　客户机启动后的登录界面.jpg)

图3-11　客户机启动后的登录界面

在通过VNC链接到QEMU窗口后，可以按组合键Ctrl+Alt+2切换到QEMU监视器窗口。在监视器窗口中可以执行一些命令，比如执行“info kvm”命令来查看当前QEMU是否使用KVM，如图3-12所示（显示为kvm support：enabled）。

图3-12　QEMU Monitor中“info kvm”命令

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\3-10.jpg)



用组合键Ctrl+Alt+1切换回普通的客户机查看窗口，就可以登录或继续使用客户机系统了。至此，你就已经启动属于自己的第一个KVM客户机了，尽情享受KVM虚拟化带来的快乐吧！

------



# 第4章　KVM核心基础功能

## 4.1　硬件平台和软件版本说明

libvirt是为了更方便地管理平台虚拟化技术而设计的开放源代码的应用程序接口、守护进程和管理工具，它不仅提供了对虚拟化客户机的管理，也提供了对虚拟化网络和存储的管理。libvirt支持多种虚拟化方案，既支持包括KVM、QEMU、Xen、VMware、VirtualBox、Hyper-V等在内的平台虚拟化方案，也支持OpenVZ、LXC等Linux容器虚拟化系统，还支持用户态Linux（UML）的虚拟化。libvirt是一个免费的开源的软件，使用的
许可证是LGPL[1]（GNU宽松的通用公共许可证）.

libvirt本身提供了一套较为稳定的C语言应用程序接口，目前，在其他一些流行的编程语言中也提供了对libvirt的绑定，在Python、Perl、Java、Ruby、PHP、OCaml等高级编程语言中已经有libvirt的程序库可以直接使用。libvirt还提供了为基于AMQP（高级消息队列协议）的消息系统（如Apache Qpid）提供QMF代理，这可以让云计算管理系统中宿主机与客户机、客户机与客户机之间的消息通信变得更易于实现。libvirt还为安全地远程管理虚拟客户机提供了加密和认证等安全措施。正是由于libvirt拥有这些强大的功能和较为稳定的应用程序接口，而且它的许可证（license）也比较宽松，所以libvirt的应用程序接口已被广泛地用在基于虚拟化和云计算的解决方案中，主要作为连接底层Hypervisor和上层应用程序的一个中间适配层。

libvirt作为中间适配层，可以让底层Hypervisor对上层用户空间的管理工具是完全透明的，因为libvirt屏蔽了底层各种Hypervisor的细节，为上层管理工具提供了一个统一的、较稳定的接口（API）。通过libvirt，一些用户空间管理工具可以管理各种不同的Hypervisor和上面运行的客户机，它们之间基本的交互框架如图4-1所示。![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图4-1　虚拟机管理工具通过libvirt管理各种类型的虚拟机.jpg)



在libvirt中涉及几个重要的概念，解释如下：

·节点（Node）是一个物理机器，上面可能运行着多个虚拟客户机。Hypervisor和Domain都运行在节点上。
·Hypervisor也称虚拟机监控器（VMM），如KVM、Xen、VMware、Hyper-V等，是虚拟化中的一个底层软件层，它可以虚拟化一个节点让其运行多个虚拟客户机（不同客户机可能有不同的配置和操作系统）。
·域（Domain）是在Hypervisor上运行的一个客户机操作系统实例。域也被称为实例（instance，如在亚马逊的AWS云计算服务中客户机就被称为实例）、客户机操作系统（guest OS）、虚拟机（virtual machine），它们都是指同一个概念。
节点、Hypervisor和域的关系可以简单地用图4-2来表示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图4-2　节点、Hypervisor和域之间的关系.jpg)

在了解了节点、Hypervisor和域的概念之后，用一句话概括libvirt的目标，那就是：为了安全高效地管理节点上的各个域，而提供一个公共的稳定的软件层。当然，这里的管理，既包括本地的管理，也包含远程的管理。具体地讲，libvirt的管理功能主要包含如下5个部分。

**1）域的管理**包括对节点上的域的各个生命周期的管理，如启动、停止、暂停、保存、恢复和动态迁移。还包括对多种设备类型的热插拔操作，包括磁盘、网卡、内存和CPU。当然不同的Hypervisor上对这些热插拔的支持程度有所不同。
**2）远程节点的管理。**只要物理节点上运行了libvirtd这个守护进程，远程的管理程序就可以连接到该节点进程管理操作，经过认证和授权之后，所有的libvirt功能都可以被访问和使用。libvirt支持多种网络远程传输类型，如SSH、TCP套接字、Unix domainsocket、TLS的加密传输等。假设使用了最简单的SSH，不需要额外的配置工作，比如，在example.com节点上运行了libvirtd，而且允许SSH访问，在远程的某台管理机器上就可以用如下的命令行来连接到example.com上，从而管理其上的域。
`virsh -c qemu+ssh://root@example.com/system`
**3）存储的管理。**任何运行了libvirtd守护进程的主机，都可以通过libvirt来管理不同类型的存储，如创建不同格式的客户机镜像（qcow2、raw、qde、vmdk等）、挂载NFS共享存储系统、查看现有的LVM卷组、创建新的LVM卷组和逻辑卷、对磁盘设备分区、挂载iSCSI共享存储、使用Ceph系统支持的RBD远程存储，等等。当然在libvirt中，对存储的管理也是支持远程的。
**4）网络的管理。**任何运行了libvirtd守护进程的主机，都可以通过libvirt来管理物理的和逻辑的网络接口。包括列出现有的网络接口卡，配置网络接口，创建虚拟网络接口，网络接口的桥接，VLAN管理，NAT网络设置，为客户机分配虚拟网络接口，等等。

**5）提供一个稳定、可靠、高效的应用程序接口，以便可以完成前面的4个管理功能。**
libvirt主要由3个部分组成，分别是：应用程序编程接口库、一个守护进程（libvirtd）和一个默认命令行管理工具（virsh）。应用程序接口是为其他虚拟机管理工具（如virsh、virt-manager等）提供虚拟机管理的程序库支持。libvirtd守护进程负责执行对节点上的域的管理工作，在用各种工具对虚拟机进行管理时，这个守护进程一定要处于运行状态中。而且这个守护进程可以分为两种：一种是root权限的libvirtd，其权限较大，可以完成所有支持的管理工作；一种是普通用户权限的libvirtd，只能完成比较受限的管理工作。virsh是libvirt项目中默认的对虚拟机管理的一个命令行工具，将在4.2节中详细介绍。

### 4.1.2　libvirt的安装与配置

**1.libvirt安装**

`[root@kvm-host ~]# rpm -qa | grep libvirt
libvirt-2.0.0-4.el7.x86_64
libvirt-client-2.0.0-4.el7.x86_64
libvirt-python-2.0.0-2.el7.x86_64
libvirt-daemon-2.0.0-4.el7.x86_64
libvirt-daemon-driver-qemu-2.0.0-4.el7.x86_64
libvirt-daemon-kvm-2.0.0-4.el7.x86_64
libvirt-daemon-config-network-2.0.0-4.el7.x86_64
省略其余libvirt相关的软件包；安装时直接运行 yum install libvirt 即可`

```
[root@kvm-host ~]# rpm -qa | grep '^qemu'
qemu-kvm-common-1.5.3-121.el7.x86_64
qemu-img-1.5.3-121.el7.x86_64
qemu-kvm-1.5.3-121.el7.x86_64
# 安装时，运行命令 yum install qemu-kvm 即可
```



**2.libvirt的配置文件**

```
[root@kvm-host libvirt]# cd /etc/libvirt/
[root@kvm-host libvirt]# ls
libvirt.conf libvirtd.conf lxc.conf nwfilter qemu qemu.conf qemu-lockd.conf storage virtlockd.conf
[root@kvm-host libvirt]# cd qemu
[root@kvm-host qemu]# ls
networks centos7u2-1.xml centos7u2-2.xml
```

几个重要的配置文件和目录。

**（1）/etc/libvirt/libvirt.conf**
libvirt.conf文件用于配置一些常用libvirt连接（通常是远程连接）的别名。和Linux中的普通配置文件一样，在该配置文件中以井号（#）开头的行是注释，如下：

```
[root@kvm-host kvm_demo]# cat /etc/libvirt/libvirt.conf
##
This can be used to setup URI aliases for frequently
# used connection URIs. Aliases may contain only the
# characters a-Z, 0-9, _, -.
##
Following the '=' may be any valid libvirt connection
# URI, including arbitrary parameters
##
This can be used to prevent probing of the hypervisor
# driver when no URI is supplied by the application.
#uri_default = "qemu:///system"
#为了演示目录，配置了如下这个别名
uri_aliases = [
"remote1=qemu+ssh://root@192.168.93.201/system",
]
```

其中，配置了remote1这个别名，用于指代qemu+ssh：//root@192.168.93.201/system这个远程的libvirt连接。有这个别名后，就可以在用virsh等工具或自己写代码调用libvirt API时使用这个别名，而不需要写完整的、冗长的URI连接标识了。用virsh使用这个别名，连接到远程的libvirt上查询当前已经启动的客户机状态，然后退出连接。命令行操作如下：



```
[root@kvm-host kvm_demo]# systemctl reload libvirtd
[root@kvm-host kvm_demo]# virsh -c remote1
root@192.168.93.201's password:
Welcome to virsh, the virtualization interactive terminal.
Type: 'help' for help with commands
		'quit' to quit
virsh # list

Id Name State

1 rhel7u2-remote running
virsh # quit
[root@kvm-host kvm_demo]#
```

在代码中调用libvirt API时也可以使用这个别名来建立连接，如下的python代码行就实现了使用这个别名来建立连接。

```
conn = libvirt.openReadOnly('remote1')
```



（2）/etc/libvirt/libvirtd.conf
libvirtd.conf是libvirt的守护进程libvirtd的配置文件，被修改后需要让libvirtd重新加载配置文件（或重启libvirtd）才会生效。在libvirtd.conf文件中，用井号（#）开头的行是注释内容，真正有用的配置在文件的每一行中使用“配置项=值”（如tcp_port="16509"）这样配对的格式来设置。在libvirtd.conf中配置了libvirtd启动时的许多设置，包括是否建立TCP、UNIX domain socket等连接方式及其最大连接数，以及这些连接的认证机制，设置libvirtd的日志级别等。

（2）/etc/libvirt/libvirtd.conf
libvirtd.conf是libvirt的守护进程libvirtd的配置文件，被修改后需要让libvirtd重新加载置文件（或重启libvirtd）才会生效。在libvirtd.conf文件中，用井号（#）开头的行是注释内容，真正有用的配置在文件的每一行中使用“配置项=值”（如tcp_port="16509"）这样配对的格式来设置。在libvirtd.conf中配置了libvirtd启动时的许多设置，包括是否建立TCP、UNIX domain socket等连接方式及其最大连接数，以及这些连接的认证机制，设置libvirtd的日志级别等。

例如，下面的几个配置项表示关闭TLS安全认证的连接（默认值是打开的），打开TCP连接（默认是关闭TCP连接的），设置TCP监听的端口，TCP连接不使用认证授权方式，设置UNIX domain socket的保存目录等。



```
listen_tls = 0
listen_tcp = 1
tcp_port = "16666"
unix_sock_dir = "/var/run/libvirt"
auth_tcp = "none"
```

注意
要让TCP、TLS等连接生效，需要在启动libvirtd时加上--listen参数（简写为-l）。而默的systemctl start libvirtd命令在启动libvirtd服务时并没带--listen参数。所以如果要使用TCP等连接方式，可以使用libvirtd--listen-d命令来启动libvirtd。以上配置选项实现将UNIX socket放到/var/run/libvirt目录下，启动libvirtd并检验配置
是否生效。命令行操作如下：

```
[root@kvm-host ~]# libvirtd --listen -d
[root@kvm-host ~]# virsh -c qemu+tcp://localhost:16666/system
Welcome to virsh, the virtualization interactive terminal.
Type: 'help' for help with commands
'quit' to quit
virsh # quit
[root@kvm-host ~]# ls /var/run/libvirt/libvirt-sock*
/var/run/libvirt/libvirt-sock /var/run/libvirt/libvirt-sock-ro
```

（3）/etc/libvirt/qemu.conf
qemu.conf是libvirt对QEMU的驱动的配置文件，包括VNC、SPICE等，以及连接它们时采用的权限认证方式的配置，也包括内存大页、SELinux、Cgroups等相关配置。
（4）/etc/libvirt/qemu/目录
在qemu目录下存放的是使用QEMU驱动的域的配置文件。查看qemu目录如下：[root@kvm-host ~]# ls /etc/libvirt/qemu/

networks centos7u2-1.xml centos7u2-2.xml

其中包括了两个域的XML配置文件（centos7u2-1.xml和centos7u2-2.xml），这就是笔者用virt-manager工具创建的两个域，默认会将其配置文件保存到/etc/libvirt/qemu/目录下。而其中的networks目录保存了创建一个域时默认使用的网络配置。

3.libvirtd的使用

libvirtd是一个作为libvirt虚拟化管理系统中的服务器端的守护程序，要让某个节点能够利用libvirt进行管理（无论是本地还是远程管理），都需要在这个节点上运行libvirtd这个守护进程，以便让其他上层管理工具可以连接到该节点，libvirtd负责执行其他管理工具发送给它的虚拟化管理操作指令。而libvirt的客户端工具（包括virsh、virt-manager等）可以连接到本地或远程的libvirtd进程，以便管理节点上的客户机（启动、关闭、重启、迁移等）、收集节点上的宿主机和客户机的配置和资源使用状态。

在RHEL 7.3中，libvirtd是作为一个服务（service）配置在系统中的，所以可以通过systemctl命令来对其进行操作（RHEL 6.x等系统中使用service命令）。常用的操作方式有：“systemctl start libvirtd”命令表示启动libvirtd，“systemctl restart libvirtd”表示重启libvirtd，“systemctl reload libvirtd”表示不重启服务但重新加载配置文件（即/etc/libvirt/libvirtd.conf配置文件），“systemctl status libvirtd”表示查询libvirtd服务的运行状态。对libvirtd服务进行操作的命令行演示如下：

```
[root@kvm-host ~]# systemctl start libvirtd
[root@kvm-host ~]#
[root@kvm-host ~]# systemctl reload libvirtd
[root@kvm-host ~]#
[root@kvm-host ~]# systemctl status libvirtd
● libvirtd.service - Virtualization daemon
Loaded: loaded (/usr/lib/systemd/system/libvirtd.service; enabled; vendor preset: enabled)
Active: active (running) since Sun 2016-11-06 20:49:45 CST; 16s ago
Docs: man:libvirtd(8)
http://libvirt.org
Process: 7387 ExecReload=/bin/kill -HUP $MAINPID (code=exited, status=0/SUCCESS)
Main PID: 7170 (libvirtd)
CGroup: /system.slice/libvirtd.service
├─2267 /sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/├─2268 /sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/└─7170 /usr/sbin/libvirtd
[root@kvm-host ~]#
[root@kvm-host ~]# systemctl stop libvirtd
[root@kvm-host ~]#
[root@kvm-host ~]# systemctl status libvirtd
● libvirtd.service - Virtualization daemon
Loaded: loaded (/usr/lib/systemd/system/libvirtd.service; enabled; vendor preset: enabled)

Active: inactive (dead) since Sun 2016-11-06 20:50:08 CST; 5s ago
```

在默认情况下，libvirtd在监听一个本地的Unix domain socket，而没有监听基于网络的TCP/IP socket，需要使用“-l或--listen”的命令行参数来开启对libvirtd.conf配置文件中TCP/IP socket的配置。另外，libvirtd守护进程的启动或停止，并不会直接影响正在运行中的客户机。libvirtd在启动或重启完成时，只要客户机的XML配置文件是存在的，libvirtd会自动加载这些客户的配置，获取它们的信息。当然，如果客户机没有基于libvirt格式的XML文件来运行（例如直接使用qemu命令行来启动的客户机），libvirtd则不能自动发现它。

libvirtd是一个可执行程序，不仅可以使用“systemctl”命令调用它作为服务来运行，而且可以单独地运行libvirtd命令来使用它。下面介绍几种libvirtd命令行的参数。

1）-d或--daemon

表示让libvirtd作为守护进程（daemon）在后台运行。

（2）-f或--config FILE

指定libvirtd的配置文件为FILE，而不是使用默认值（通常是/etc/libvirt/libvirtd.conf）。
（3）-l或--listen

开启配置文件中配置的TCP/IP连接。

（4）-p或--pid-file FILE

将libvirtd进程的PID写入FILE文件中，而不是使用默认值（通常是/var/run/libvirtd.pid）。

（5）-t或--timeout SECONDS

设置对libvirtd连接的超时时间为SECONDS秒。

（6）-v或--verbose

执行命令输出详细的输出信息。特别是在运行出错时，详细的输出信息便于用户查找原因。

（7）--version

显示libvirtd程序的版本信息。

关于于libvirtd命令的使用，几个简单的命令行操作演示如下：

```
#使用libvirtd 命令前，先停止已运行的服务
[root@kvm-host ~]# systemctl stop libvirtd
[root@kvm-host ~]# libvirtd --version
libvirtd (libvirt) 2.0.0
[root@kvm-host ~]# libvirtd
^C #没有以daemon的形式启动，标准输出被libvirtd占用；这里用Ctrl+C组合键结束libvirtd进程，以便继续进行后续操作
[root@kvm-host ~]# libvirtd -l -d -p /root/libvirtd.pid
[root@kvm-host ~]# cat /root/libvirtd.pid
8136
```

### 4.1.3　libvirt域的XML配置文件

在使用libvirt对虚拟化系统进行管理时，很多地方都是以XML文件作为配置文件的，包括客户机（域）的配置、宿主机网络接口配置、网络过滤、各个客户机的磁盘存储配置、磁盘加密、宿主机和客户机的CPU特性，等等。本节只针对客户机的XML进行较详细介绍，因为客户机的配置是最基本的和最重要的，了解了它之后就可以使用libvirt管理客户机了。

#### **1.客户机的XML配置文件格式的示例**

在libvirt中，客户机（即域）的配置是采用XML格式来描述的。下面展示了笔者使用virt-manager创建的一个客户机的配置文件（即在4.1.2节中看到的centos7u2-1.xml文件），后面几节将会分析其中的主要配置项目。

```
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
virsh edit centos7u2-1
or other application using the libvirt API.
-->
<domain type='kvm'>
<name>centos7u2-1</name>
<uuid>2f6260bf-1283-4933-aaef-fa82148537ba</uuid>
<memory unit='KiB'>2097152</memory>
<currentMemory unit='KiB'>2097152</currentMemory>
<vcpu placement='static'>2</vcpu>
<os>
<type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
<boot dev='hd'/>
<boot dev='cdrom'/>
</os>
<features>
<acpi/>
<apic/>
</features>
<cpu mode='custom' match='exact'>
<model fallback='allow'>Haswell-noTSX</model>
</cpu>
<clock offset='utc'>
<timer name='rtc' tickpolicy='catchup'/>
<timer name='pit' tickpolicy='delay'/>
<timer name='hpet' present='no'/>
</clock>
<on_poweroff>destroy</on_poweroff>
<on_reboot>restart</on_reboot>
<on_crash>restart</on_crash>
<pm>
<suspend-to-mem enabled='no'/>
<suspend-to-disk enabled='no'/>
</pm>
<devices>
<emulator>/usr/libexec/qemu-kvm</emulator>
<disk type='file' device='disk'>
<driver name='qemu' type='qcow2' cache='none'/>
<source file='/var/lib/libvirt/images/centos7u2.qcow2'/>
<target dev='vda' bus='virtio'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>

</disk>
<controller type='usb' index='0' model='ich9-ehci1'>

<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function= '0x7'/>

</controller>
<controller type='usb' index='0' model='ich9-uhci1'>
<master startport='0'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function= '0x0' multifunction='on'/>

</controller>
<controller type='usb' index='0' model='ich9-uhci2'>
<master startport='2'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function= '0x1'/>

</controller>
<controller type='usb' index='0' model='ich9-uhci3'>
<master startport='4'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x2'/>

</controller>
<controller type='pci' index='0' model='pci-root'/>
<controller type='virtio-serial' index='0'>

<address type='pci' domain='0x0000' bus='0x00' slot='0x05' function= '0x0'/>

</controller>
<interface type='network'>
<mac address='52:54:00:36:32:aa'/>
<source network='default'/>
<model type='virtio'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x03' function= '0x0'/>

</interface>
<serial type='pty'>
<target port='0'/>
</serial>
<console type='pty'>
<target type='serial' port='0'/>
</console>
<channel type='unix'>
<source mode='bind' path='/var/lib/libvirt/qemu/channel/target/domain- centos7u2/org.qemu.guest_agent.<target type='virtio' name='org.qemu.guest_agent.0'/>

<address type='virtio-serial' controller='0' bus='0' port='1'/>

</channel>
<channel type='spicevmc'>
<target type='virtio' name='com.redhat.spice.0'/>

<address type='virtio-serial' controller='0' bus='0' port='2'/>

</channel>
<input type='tablet' bus='usb'/>
<input type='mouse' bus='ps2'/>
<input type='keyboard' bus='ps2'/>
<graphics type='vnc' port='-1' autoport='yes'/>
<sound model='ich6'>

<address type='pci' domain='0x0000' bus='0x00' slot='0x04' function= '0x0'/>

</sound>

<video>
<model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x02' function= '0x0'/>
</video>

<redirdev bus='usb' type='spicevmc'>
</redirdev>
<redirdev bus='usb' type='spicevmc'>
</redirdev>
<memballoon model='virtio'>

<address type='pci' domain='0x0000' bus='0x00' slot='0x08' function= '0x0'/>

</memballoon>
</devices>
</domain>
```

由上面的配置文件示例可以看到，在该域的XML文件中，所有有效配置都在<domain>和</domain>标签之间，这表明该配置文件是一个域的配置。（XML文档中的注释在两个特殊的标签之间，如<！--注释-->。）

通过libvirt启动客户机，经过文件解析和命令参数的转换，最终也会调用qemu命令行工具来实际完成客户机的创建。用这个XML配置文件启动的客户机，它的qemu命令行参数是非常详细、非常冗长的一行。查询qemu命令行参数的操作如下：

```
[root@kvm-host ~]# ps -ef | grep qemu | grep centos7u2-1
qemu 5865 1 60 21:21 ? 00:00:13 /usr/libexec/qemu-kvm -name centos7u2-1 -S -machine pc-i440fx-rhel7.0.0,
```

这里RHEL 7.3系统中默认的QEMU工具为/usr/libexec/qemu-kvm，与第3章中从源代码编译和安装的qemu-system-x86_64工具是类似的，它们的参数也基本一致（当然如果二者版本差异较大，参数和功能可能有一些不同）。对于qemu命令的这么多参数，本书其他章节中会介绍，本节主要针对域的XML配置文件进行介绍和分析。

#### **2.CPU、内存、启动顺序等基本配置**

**1）CPU的配置**

前面介绍的centos7u2-1.xml配置文件中，关于CPU的配置如下：

```
<vcpu placement='static'>2</vcpu>
<features>
<acpi/>
<apic/>
</features>
<cpu mode='custom' match='exact'>
<model fallback='allow'>Haswell-noTSX</model>
</cpu>
```

vcpu标签，表示客户机中vCPU的个数，这里为2。features标签，表示Hypervisor为客户机打开或关闭CPU或其他硬件的特性，这里打开了ACPI、APIC等特性。当然，CPU的基础特性是在cpu标签中定义的，这里是之前创建客户机时，libvirt自动检测了CPU硬件平台，默认使用了Haswell的CPU给客户机。对于这里看到的CPU模型：Haswell-noTSX，可以在文件/usr/share/libvirt/cpu_map.xml中查看详细描述。该CPU模型中的特性（如SSE2、
LM、NX、TSC、AVX2、SMEP等）也是该客户机可以看到和使用的特性。

**对于CPU模型的配置，有以下3种模式。**

1）custom模式：就是这里示例中表示的，基于某个基础的CPU模型，再做个性化的设置。
2）host-model模式：根据物理CPU的特性，选择一个与之最接近的标准CPU型号，如果没有指定CPU模式，默认也是使用这种模式。xml配置文件为：<cpu mode='hostmodel'/>。
3）host-passthrough模式：直接将物理CPU特性暴露给虚拟机使用，在虚拟机上看到的完全就是物理CPU的型号。xml配置文件为：<cpu mode='host-passthrough'/>。对vCPU的分配，可以有更细粒度的配置，如下：

```
<memballoon model='virtio'>
<domain>
...
<vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu>
...
</domain>
```

cpuset表示允许到哪些物理CPU上执行，这里表示客户机的两个vCPU被允许调度到1、2、4、6号物理CPU上执行（^3表示排除3号）；而current表示启动客户机时只给1个vCPU，最多可以增加到使用2个vCPU。
当然，libvirt还提供cputune标签来对CPU的分配进行更多调节，如下：

<domain>
...
<cputune>
<vcpupin vcpu="0" cpuset="1"/>
<vcpupin vcpu="1" cpuset="2,3"/>
<vcpupin vcpu="2" cpuset="4"/>
<vcpupin vcpu="3" cpuset="5"/>
<emulatorpin cpuset="1-3"/>
<shares>2048</shares>
<period>1000000</period>
<quota>-1</quota>
<emulator_period>1000000</emulator_period>
<emulator_quota>-1</emulator_quota>
</cputune>
...
</domain>
这里只简单解释其中几个配置：vcpupin标签表示将虚拟CPU绑定到某一个或多个物
理CPU上，如“<vcpupin vcpu="2"cpuset="4"/>”表示客户机2号虚拟CPU被绑定到4号物理
CPU上；“<emulatorpin cpuset="1-3"/>”表示将QEMU emulator绑定到1~3号物理CPU上。在
不设置任何vcpupin和cpuset的情况下，客户机的虚拟CPU可能会被调度到任何一个物理
CPU上去运行。“<shares>2048</shares>”表示客户机占用CPU时间的加权配置，一个配置
为2048的域获得的CPU执行时间是配置为1024的域的两倍。如果不设置shares值，就会使
用宿主机系统提供的默认值。
另外，还可以配置客户机的NUMA拓扑，以及让客户机针对宿主机NUMA的策略设
置等，读者可参考<numa>标签和<numatune>标签。

（2）内存的配置
在该域的XML配置文件中，内存大小的配置如下：
<memory unit='KiB'>2097152</memory>
<currentMemory unit='KiB'>2097152</currentMemory>
可知，内存大小为2 097 152KB（即2GB），memory标签中的内存表示客户机最大可
使用的内存，currentMemory标签中的内存表示启动时即分配给客户机使用的内存。在使
用QEMU/KVM时，一般将二者设置为相同的值。
另外，内存的ballooning相关的配置包含在devices这个标签的memballoon子标签中，
该标签配置了该客户机的内存气球设备，如下：

<memballoon model='virtio'>
<address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>
</memballoon>
该配置将为客户机分配一个使用virtio-balloon驱动的设备，以便实现客户机内存的
ballooning调节。该设备在客户机中的PCI设备编号为0000：00：08.0。
（3）客户机系统类型和启动顺序
客户机系统类型及其启动顺序在os标签中配置，如下：
<os>
<type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
<boot dev='hd'/>
<boot dev='cdrom'/>
</os>
这样的配置表示客户机类型是hvm类型，HVM（hardware virtual machine，硬件虚拟
机）原本是Xen虚拟化中的概念，它表示在硬件辅助虚拟化技术（Intel VT或AMD-V等）
的支持下不需要修改客户机操作系统就可以启动客户机。因为KVM一定要依赖于硬件虚
拟化技术的支持，所以在KVM中，客户机类型应该总是hvm，操作系统的架构是
x86_64，机器类型是pc-i440fx-rhel7.0.0（这是libvirt中针对RHEL 7系统的默认类型，也可
以根据需要修改为其他类型）。boot选项用于设置客户机启动时的设备，这里有hd（即硬
盘）和cdrom（光驱）两种，而且是按照硬盘、光驱的顺序启动的，它们在XML配置文件
中的先后顺序即启动时的先后顺序。

```

```



type='bridge'表示使用桥接方式使客户机获得网络，address用于配置客户机中网卡的MAC地址，<source bridge='br0'/>表示使用宿主机中的br0网络接口来建立网桥，<modeltype='virtio'/>表示在客户机中使用virtio-net驱动的网卡设备，也配置了该网卡在客户机中的PCI设备编号为0000：00：03.0。

3.网络的配置
（1）桥接方式的网络配置
在域的XML配置中，使用桥接方式的网络的相关配置如下：

<devices>
...
<interface type='bridge'>
<mac address='52:54:00:e9:e0:3b'/>
<source bridge='br0'/>
<model type='virtio'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
...
</devices>
type='bridge'表示使用桥接方式使客户机获得网络，address用于配置客户机中网卡的
MAC地址，<source bridge='br0'/>表示使用宿主机中的br0网络接口来建立网桥，<model
type='virtio'/>表示在客户机中使用virtio-net驱动的网卡设备，也配置了该网卡在客户机中
的PCI设备编号为0000：00：03.0

**（2）NAT方式的虚拟网络配置**

在域的XML配置中，NAT方式的虚拟网络的配置示例如下：

```
<devices>
...
<interface type='network'>
<mac address='52:54:00:32:7d:f6'/>
<source network='default'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>

</interface>
...
</devices>
```

这里type='network'和<source network='default'/>表示使用NAT的方式，并使用默认的
网络配置，客户机将会分配到192.168.122.0/24网段中的一个IP地址。当然，使用NAT必须
保证宿主机中运行着DHCP和DNS服务器，一般默认使用dnsmasq软件查询。查询DHCP和
DNS服务的运行的命令行如下：
[root@kvm-host ~]# ps -ef | grep dnsmasq
nobody 1863 1 0 Dec08 ? 00:00:03 /usr/sbin/dnsmasq --strict-order --bind-interfaces --pid-file=/var/由于配置使用了默认的NAT网络配置，可以在libvirt相关的网络配置中看到一个
default.xml文件（/etc/libvirt/qemu/networks/default.xml），它具体配置了默认的连接方
式，如下：

```
<network>
<name>default</name>
<bridge name="virbr0" />
<forward/>
<ip address="192.168.122.1" netmask="255.255.255.0">
<dhcp>
<range start="192.168.122.2" end="192.168.122.254" />
</dhcp>
</ip>
</network>
```

在使用NAT时，查看宿主机中网桥的使用情况如下：




```
root@kvm-host ~]# brctl show
bridge name bridge id STP enabled interfaces
virbr0 8000.525400b45ba5 yes virbr0-nic
vnet0
```

其中vnet0这个网络接口就是客户机和宿主机网络连接的纽带。

**（3）用户模式网络的配置**

在域的XML文件中，如下的配置即实现了使用用户模式的网络。

```
<devices>
...
<interface type='user'>
<mac address="00:11:22:33:44:55"/>
</interface>
...
</devices>
```

其中，type='user'表示该客户机的网络接口是用户模式网络，是完全由QEMU软件模拟的一个网络协议栈。在宿主机中，没有一个虚拟的网络接口连接到virbr0这样的网桥。

**（4）网卡设备直接分配（VT-d）**

在客户机的网络配置中，还可以采用PCI/PCI-e网卡将设备直接分配给客户机使用。关于设备直接分配的细节，可以参考6.2节中的介绍，本节只介绍其在libvirt中的配置方式。对于设备直接分配的配置在域的XML配置文件中有两种方式：一种是较新的方式，使用<interface type='hostdev'/>标签；另一种是较旧但支持设备很广泛的方式，直接使用<hostdev>标签。

<interface type='hostdev'/>标签是较新的配置方式，目前仅支持libvirt 0.9.11以上的版本，而且仅支持SR-IOV特性中的VF的直接配置。在<interface type='hostdev'/>标签中，用<driver name='vfio'/>指定使用哪一种分配方式（默认是VFIO，如果使用较旧的传统的device assignment方式，这个值可配为'kvm'），用<source>标签来指示将宿主机中的哪个VF分配给宿主机使用，还可使用<mac address='52：54：00：6d：90：02'>来指定在客户机中看到的该网卡设备的MAC地址。一个示例配置如下所示，它表示将宿主机的0000：08：10.0这个VF网卡直接分配给客户机使用，并规定该网卡在客户机中的MAC地址为“52：54：00：6d：90：02”。

<devices>
...
<interface type='hostdev'>
<driver name='vfio'/>
<source>

<address type='pci' domain='0x0000' bus='0x08' slot='0x10' function= '0x0'/>
</source>
<mac address='52:54:00:6d:90:02'>
</interface>
...
</devices>

在<devices>标签中使用<hostdev>标签来指定将网卡设备直接分配给客户机使用，这是较旧的配置方式，是libvirt 0.9.11版本之前对设备直接分配的唯一使用方式，而且对设备的支持较为广泛，既支持有SR-IOV功能的高级网卡的VF的直接分配，也支持无SR-IOV功能的普通PCI或PCI-e网卡的直接分配。这种方式并不支持对直接分配的网卡在客户机中的MAC地址的设置，在客户机中网卡的MAC地址与宿主机中看到的完全相同。在域的XML配置文件中，使用<hostdev>标签配置网卡设备直接分配的示例如下所示，它表示将宿主机中的PCI 0000：08：00.0设备直接分配给客户机使用。

<devices>
...
<hostdev mode='subsystem' type='pci' managed='yes'>
<source>

<address domain='0x0000' bus='0x08' slot='0x00' function='0x0'/>
</source>
</hostdev>
...
</devices>

#### 4.存储的配置

在示例的域的XML配置文件中，关于客户机磁盘的配置如下：

<devices>
...
<disk type='file' device='disk'>
<driver name='qemu' type='qcow2' cache='none'/>
<source file='/var/lib/libvirt/images/centos7u2.qcow2'/>
<target dev='vda' bus='virtio'/>

<address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
</disk>
...
</devices>
上面的配置表示，使用qcow2格式的centos7u2.qcow镜像文件作为客户机的磁盘，其
在客户机中使用virtio总线（使用virtio-blk驱动），设备名称为/dev/vda，其PCI地址为
0000：00：07.0。
<disk>标签是客户机磁盘配置的主标签，其中包含它的属性和一些子标签。它的type
属性表示磁盘使用哪种类型作为磁盘的来源，其取值为file、block、dir或network中的一
个，分别表示使用文件、块设备、目录或网络作为客户机磁盘的来源。它的device属性表
示让客户机如何来使用该磁盘设备，其取值为floppy、disk、cdrom或lun中的一个，分别
表示软盘、硬盘、光盘和LUN（逻辑单元号），默认值为disk（硬盘）。
在<disk>标签中可以配置许多子标签，这里仅简单介绍一下上面示例中出现的几个重
要的子标签。<driver>子标签用于定义Hypervisor如何为该磁盘提供驱动，它的name属性
用于指定宿主机中使用的后端驱动名称，QEMU/KVM仅支持name='qemu'，但是它支持的
类型type可以是多种，包括raw、qcow2、qed、bochs等。而这里的cache属性表示在宿主机
中打开该磁盘时使用的缓存方式，可以配置为default、none、writethrough、writeback、
directsync和unsafe等多种模式。在5.4.1节中已经详细地介绍过磁盘缓存的各种配置方式的
区别。
<source>子标签表示磁盘的来源，当<disk>标签的type属性为file时，应该配置为
<source file='/var/lib/libvirt/images/centos7u2-1.img'/>这样的模式，而当type属性为block
时，应该配置为<source dev='/dev/sda'/>这样的模式。
<target>子标签表示将磁盘暴露给客户机时的总线类型和设备名称。其dev属性表示在
客户机中该磁盘设备的逻辑设备名称，而bus属性表示该磁盘设备被模拟挂载的总线类
型，bus属性的值可以为ide、scsi、virtio、xen、usb、sata等。如果省略了bus属性，libvirt
则会根据dev属性中的名称来“推测”bus属性的值，例如，sda会被推测是scsi，而vda被推测
是virtio。
<address>子标签表示该磁盘设备在客户机中的PCI总线地址，这个标签在前面网络配
置中也是多次出现的，如果该标签不存在，libvirt会自动分配一个地址。
5.其他配置简介
（1）域的配置
在域的整个XML配置文件中，<domain>标签是范围最大、最基本的标签，是其他所
有标签的根标签。在示例的域的XML配置文件中，<domain>标签的配置如下：
<domain type='kvm'>
...
</domain>
在<domain>标签中可以配置两个属性：一个是type，用于表示Hypervisor的类型，可
选的值为xen、kvm、qemu、lxc、kqemu、VMware中的一个；另一个是id，其值是一个数
字，用于在该宿主机的libvirt中唯一标识一个运行着的客户机，如果不设置id属性，libvirt
会按顺序分配一个最小的可用ID。
（2）域的元数据配置
在域的XML文件中，有一部分是用于配置域的元数据（meta data）。元数据用于表
示域的属性（用于区别其他的域）。在示例的域的XML文件中，元数据的配置如下：
<name>centos7u2-1</name>
<uuid>2f6260bf-1283-4933-aaef-fa82148537ba</uuid>
其中，name用于表示该客户机的名称，uuid是唯一标识该客户机的UUID。在同一个
宿主机上，各个客户机的名称和UUID都必须是唯一的。
当然，域的元数据还有其他很多配置，例如Xen上的一个域的元数据配置如下：
<domain type='xen' id='3'>
<name>fv0</name>
<uuid>4dea22b31d52d8f32516782e98ab3fa0</uuid>
<title>A short description - title - of the domain</title>
<description>Some human readable description</description>
<metadata>
<app1:foo xmlns:app1="http://app1.org/app1/">..</app1:foo>
<app2:bar xmlns:app2="http://app1.org/app2/">..</app2:bar>
</metadata>
...
</domain>
（3）QEMU模拟器的配置
在域的配置文件中，需要制定使用的设备模型的模拟器，在emulator标签中配置模拟
器的绝对路径。在示例的域的XML文件中，模拟器的配置如下：
<devices>
<emulator>/usr/libexec/qemu-kvm</emulator>
...
</devices>
假设自己编译了一个最新的QEMU，要使用自己编译的QEMU作为模拟器，只需要将
这里修改为/usr/local/bin/qemu-system-x86_64即可。不过，创建客户机时可能会遇到如下
的错误信息：
[root@kvm-host ~]# virsh create rhel7u2-1.xml
error: Failed to create domain from rhel7u2-1.xml
error: internal error Process exited while reading console log output: Supported machines are:
pc Standard PC (alias of pc-1.1)
pc-1.1 Standard PC (default)
pc-1.0 Standard PC
pc-0.15 Standard PC
pc-0.14 Standard PC
pc-0.13 Standard PC
这是因为自己编译的qemu-system-x86_64并不支持配置文件中的pc-i440fx-rhel7.0.0机
器类型。做如下修改即可解决这个问题：
<type arch='x86_64' machine='pc'>hvm</type>
（4）图形显示方式
在示例的域的XML文件中，对连接到客户机的图形显示方式的配置如下：
<devices>
...
<graphics type='vnc' port='-1' autoport='yes'/>
...
</devices>
这表示通过VNC的方式连接到客户机，其VNC端口为libvirt自动分配。
也可以支持其他多种类型的图形显示方式，以下就配置了SDL、VNC、RDP、SPICE
等多种客户机显示方式。
<devices>
...
<graphics type='sdl' display=':0.0'/>
<graphics type='vnc' port='5904'>
<listen type='address' address='1.2.3.4'/>
</graphics>
<graphics type='rdp' autoport='yes' multiUser='yes' />
<graphics type='desktop' fullscreen='yes'/>
<graphics type='spice'>
<listen type='network' network='rednet'/>
</graphics>
...
</devices>
（5）客户机声卡和显卡的配置
在示例的域的XML文件中，该客户机的声卡和显卡的配置如下：
<devices>
...
<sound model='ich6'>
<address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
</sound>
<video>
<model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
</video>
...
</devices>
<sound>标签表示的是声卡配置，其中model属性表示为客户机模拟出来的声卡的类
型，其取值为es1370、sb16、ac97和ich6中的一个。
<video>标签表示的是显卡配置，其中<model>子标签表示为客户机模拟的显卡的类
型，它的类型（type）属性可以为vga、cirrus、vmvga、xen、vbox、qxl中的一个，vram属
性表示虚拟显卡的显存容量（单位为KB），heads属性表示显示屏幕的序号。本示例中，
KVM客户机的显卡的配置为qxl类型、显存为65536（即64 MB）、使用在第1号屏幕上。
（6）串口和控制台
串口和控制台是非常有用的设备，特别是在调试客户机的内核或遇到客户机宕机的情
况下，一般都可以在串口或控制台中查看到一些利于系统管理员分析问题的日志信息。在
示例的域的XML文件中，客户机串口和控制台的配置如下：
<devices>
...
<serial type='pty'>
<target port='0'/>
</serial>
<console type='pty'>
<target type='serial' port='0'/>
</console>
...
</devices>
设置了客户机的编号为0的串口（即/dev/ttyS0），使用宿主机中的伪终端（pty），由
于这里没有指定使用宿主机中的哪个虚拟终端，因此libvirt会自己选择一个空闲的虚拟终
端（可能为/dev/pts/下的任意一个）。当然也可以加上<source path='/dev/pts/1'/>配置来明
确指定使用宿主机中的哪一个虚拟终端。在通常情况下，控制台（console）配置在客户
机中的类型为'serial'，此时，如果没有配置串口（serial），则会将控制台的配置复制到串
口配置中，如果已经配置了串口（本例即是如此），则libvirt会忽略控制台的配置项。
当然为了让控制台有输出信息并且能够与客户机交互，也需在客户机中配置将信息输
出到串口，如在Linux客户机内核的启动行中添加“console=ttyS0”这样的配置。在9.5.2节
对-serial参数的介绍中有更多和串口配置相关的内容。
（7）输入设备
在示例的XML文件中，在客户机图形界面下进行交互的输入设备的配置如下：
<devices>
...
<input type='tablet' bus='usb'/>
<input type='mouse' bus='ps2'/>
<input type='keyboard' bus='ps2'/>
...
</devices>
这里的配置会让QEMU模拟PS2接口的鼠标和键盘，还提供了tablet这种类型的设备，
让光标可以在客户机获取绝对位置定位。在5.6.3节中将介绍tablet设备的使用及其带来的
好处。
（8）PCI控制器
根据客户机架构的不同，libvirt默认会为客户机模拟一些必要的PCI控制器（而不需要
在XML配置文件中指定），而一些PCI控制器需要显式地在XML配置文件中配置。在示例
的域的XML文件中，一些PCI控制器的配置如下：
<controller type='usb' index='0' model='ich9-ehci1'>
<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x7'/>
</controller>
<controller type='usb' index='0' model='ich9-uhci1'>
<master startport='0'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0' multifunction='on'/>
</controller>
<controller type='usb' index='0' model='ich9-uhci2'>
<master startport='2'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x1'/>
</controller>
<controller type='usb' index='0' model='ich9-uhci3'>
<master startport='4'/>
<address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x2'/>
</controller>
<controller type='pci' index='0' model='pci-root'/>
<controller type='virtio-serial' index='0'>
<address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
</controller>
这里显式指定了4个USB控制器、1个pci-root和1个virtio-serial控制器。libvirt默认还会
为客户机分配一些必要的PCI设备，如PCI主桥（Host bridge）、ISA桥等。使用示例的域
的XML配置文件启动客户机，在客户机中查看到的PCI信息如下：
[root@rhel7u2-1 ~]# lspci
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
00:01.1 IDE interface: Intel Corporation 82371SB PIIX3 IDE [Natoma/Triton II]
00:01.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 03)
00:02.0 VGA compatible controller: Redhat, Inc. QXL paravirtual graphic card (rev 04)
00:03.0 Ethernet controller: Redhat, Inc Virtio network device
00:04.0 Audio device: Intel Corporation 82801FB/FBM/FR/FW/FRW (ICH6 Family) High Definition Audio Controller (rev 00:05.0 Communication controller: Redhat, Inc Virtio console
00:06.0 USB controller: Intel Corporation 82801I (ICH9 Family) USB UHCI Controller #1 (rev 03)
00:06.1 USB controller: Intel Corporation 82801I (ICH9 Family) USB UHCI Controller #2 (rev 03)
00:06.2 USB controller: Intel Corporation 82801I (ICH9 Family) USB UHCI Controller #3 (rev 03)
00:06.7 USB controller: Intel Corporation 82801I (ICH9 Family) USB2 EHCI Controller #1 (rev 03)
00:07.0 SCSI storage controller: Redhat, Inc Virtio block device
00:08.0 Unclassified device [00ff]: Redhat, Inc Virtio memory balloon
4.1.4　libvirt API简介
libvirt的核心价值和主要目标就是提供一套管理虚拟机的、稳定的、高效的应用程序
接口（API）。libvirt API[1]本身是用C语言实现的，本节以其提供的最核心的C语言接口
的API为例进行简单的介绍。
libvirt API大致可划分为如下8个部分。
1）连接Hypervisor相关的API：以virConnect开头的一系列函数。
只有在与Hypervisor建立连接之后，才能进行虚拟机管理操作，所以连接Hypervisor的
API是其他所有API使用的前提条件。与Hypervisor建立的连接为其他API的执行提供了路
径，是其他虚拟化管理功能的基础。通过调用virConnectOpen函数可以建立一个连接，其
返回值是一个virConnectPtr对象，该对象就代表到Hypervisor的一个连接；如果连接出
错，则返回空值（NULL）。而virConnectOpenReadOnly函数会建立一个只读的连接，在
该连接上可以使用一些查询的功能，而不使用创建、修改等功能。virConnectOpenAuth函
数提供了根据认证建立的连接。virConnectGetCapabilities函数返回对Hypervisor和驱动的
功能描述的XML格式的字符串。virConnectListDomains函数返回一列域标识符，它们代表
该Hypervisor上的活动域。
2）域管理的API：以virDomain开头的一系列函数。
虚拟机最基本的管理职能就是对各个节点上的域的管理，故在libvirt API中实现了很
多针对域管理的函数。要管理域，首先要获取virDomainPtr这个域对象，然后才能对域进
行操作。有很多种方式来获取域对象，如virDomainPtr
virDomainLookupByID(virConnectPtr conn，int id)函数是根据域的id值到conn这个连接上去
查找相应的域。类似的，virDomainLookupByName、virDomainLookupByUUID等函数分
别是根据域的名称和UUID去查找相应的域。在得到某个域的对象后，就可以进行很多操
作，可以查询域的信息（如virDomainGetHostname、virDomainGetInfo、
virDomainGetVcpus、virDomainGetVcpusFlags、virDomainGetCPUStats等），也可以控制
域的生命周期（如virDomainCreate、virDomainSuspend、virDomainResume、
virDomainDestroy、virDomainMigrate等）。
3）节点管理的API：以virNode开头的一系列函数。
域运行在物理节点之上，libvirt也提供了对节点进行信息查询和控制的功能。节点管
理的多数函数都需要使用一个连接Hypervisor的对象作为其中的一个传入参数，以便可以
查询或修改该连接上的节点信息。virNodeGetInfo函数是获取节点的物理硬件信息，
virNodeGetCPUStats函数可以获取节点上各个CPU的使用统计信息，
virNodeGetMemoryStats函数可以获取节点上的内存的使用统计信息，
virNodeGetFreeMemory函数可以获取节点上可用的空闲内存大小。还有一些设置或者控制
节点的函数，如virNodeSetMemoryParameters函数可以设置节点上的内存调度的参数，
virNodeSuspendForDuration函数可以让节点（宿主机）暂停运行一段时间。
4）网络管理的API：以virNetwork开头的一系列函数和部分以virInterface开头的函
数。
libvirt也对虚拟化环境中的网络管理提供了丰富的API。libvirt首先需要创建
virNetworkPtr对象，然后才能查询或控制虚拟网络。查询网络相关信息的函数有，
virNetworkGetName函数可以获取网络的名称，virNetworkGetBridgeName函数可以获取该
网络中网桥的名称，virNetworkGetUUID函数可以获取网络的UUID标识，
virNetworkGetXMLDesc函数可以获取网络的以XML格式的描述信息，virNetworkIsActive
函数可以查询网络是否正在使用中。控制或更改网络设置的函数有，
virNetworkCreateXML函数可以根据提供的XML格式的字符串创建一个网络（返回
virNetworkPtr对象），virNetworkDestroy函数可以销毁一个网络（同时也会关闭使用该网
络的域），virNetworkFree函数可以回收一个网络（但不会关闭正在运行的域），
virNetworkUpdate函数可根据提供XML格式的网络配置来更新一个已存在的网络。另外，
virInterfaceCreate、virInterfaceFree、virInterfaceDestroy、virInterfaceGetName、
virInterfaceIsActive等函数可以用于创建、释放和销毁网络接口，以及查询网络接口的名
称和激活状态。
5）存储卷管理的API：以virStorageVol开头的一系列函数。
libvirt对存储卷（volume）的管理主要是对域的镜像文件的管理，这些镜像文件的格
式可能是raw、qcow2、vmdk、qed等。libvirt对存储卷的管理，首先需要创建
virStorageVolPtr这个存储卷对象，然后才能对其进行查询或控制操作。libvirt提供了3个函
数来分别通过不同的方式来获取存储卷对象，如virStorageVolLookupByKey函数可以根据
全局唯一的键值来获得一个存储卷对象，virStorageVolLookupByName函数可以根据名称
在一个存储资源池（storage pool）中获取一个存储卷对象，virStorageVolLookupByPath函
数可以根据它在节点上的路径来获取一个存储卷对象。有一些函数用于查询存储卷的信
息，如virStorageVolGetInfo函数可以查询某个存储卷的使用情况，virStorageVolGetName
函数可以获取存储卷的名称，virStorageVolGetPath函数可以获取存储卷的路径，
virStorageVolGetConnect函数可以查询存储卷的连接。一些函数用于创建和修改存储卷，
如virStorageVolCreateXML函数可以根据提供的XML描述来创建一个存储卷，
virStorageVolFree函数可以释放存储卷的句柄（但是存储卷依然存在），
virStorageVolDelete函数可以删除一个存储卷，virStorageVolResize函数可以调整存储卷的
大小。
6）存储池管理的API：以virStoragePool开头的一系列函数。
libvirt对存储池（pool）的管理包括对本地的基本文件系统、普通网络共享文件系
统、iSCSI共享文件系统、LVM分区等的管理。libvirt需要基于virStoragePoolPtr这个存储
池对象才能进行查询和控制操作。一些函数可以通过查询获取一个存储池对象，如
virStoragePoolLookupByName函数可以根据存储池的名称来获取一个存储池对象，
virStoragePoolLookupByVolume可以根据一个存储卷返回其对应的存储池对象。
virStoragePoolCreateXML函数可以根据XML描述来创建一个存储池（默认已激活），
virStoragePoolDefineXML函数可以根据XML描述信息静态地定义一个存储池（尚未激
活），virStorage PoolCreate函数可以激活一个存储池。virStoragePoolGetInfo、
virStoragePoolGetName、virStoragePoolGetUUID函数可以分别获取存储池的信息、名称和
UUID标识。virStoragePool IsActive函数可以查询存储池状态是否处于使用中，
virStoragePoolFree函数可以释放存储池相关的内存（但是不改变其在宿主机中的状态），
virStoragePoolDestroy函数可以用于销毁一个存储池（但并没有释放virStoragePoolPtr对
象，之后还可以用virStoragePoolCreate函数重新激活它），virStoragePoolDelete函数可以
物理删除一个存储池资源（该操作不可恢复）。
7）事件管理的API：以virEvent开头的一系列函数。
libvirt支持事件机制，在使用该机制注册之后，可以在发生特定的事件（如域的启
动、暂停、恢复、停止等）时得到自己定义的一些通知。
8）数据流管理的API：以virStream开头的一系列函数。
libvirt还提供了一系列函数用于数据流的传输。
对于libvirt API一些细节的使用方法和实现原理，可以参考其源代码。
[1] libvirt官方网站上关于libvirt API的详细描述：http://libvirt.org/html/libvirt-libvirt.html。
4.1.5　建立到Hypervisor的连接
要使用libvirt API进行虚拟化管理，就必须先建立到Hypervisor的连接，因为有了连接
才能管理节点、Hypervisor、域、网络等虚拟化中的要素。本节就介绍一下建立到
Hypervisor连接的一些方式。
对于一个libvirt连接，可以使用简单的客户端-服务器端（C/S）的架构模式来解释，
一个服务器端运行着Hypervisor，一个客户端去连接服务器端的Hypervisor，然后进行相应
的虚拟化管理。当然，如果通过libvirt API实现本地的管理，则客户端和服务器端都在同
一个节点上，并不依赖于网络连接。一般来说（如基于QEMU/KVM的虚拟化方案），不
管是基于libvirt API的本地管理还是远程管理，在服务器端的节点上，除了需要运行相应
的Hypervisor以外，还需要让libvirtd这个守护进程处于运行中的状态，以便让客户端连接
到libvirtd，从而进行管理操作。不过，也并非所有的Hypervisor都需要运行libvirtd守护进
程，比如VMware ESX/ESXi就不需要在服务器端运行libvirtd，依然可以通过libvirt客户端
以另外的方式[1]连接到VMware。
由于支持多种Hypervisor，libvirt需要通过唯一的标识来指定如何才能准确地连接到本
地或远程的Hypervisor。为了达到这个目的，libvirt使用了在互联网应用中广泛使用的
URI[2]（Uniform Resource Identifier，统一资源标识符）来标识到某个Hypervisor的连接。
libvirt中连接的标识符URI，其本地URI和远程URI有一些区别，下面分别介绍一下它们的
使用方式。
1.本地URI
在libvirt的客户端使用本地的URI连接本系统范围内的Hypervisor，本地URI的一般格
式如下：
driver[+transport]:///[path][?extral-param]
其中，driver是连接Hypervisor的驱动名称（如qemu、xen、xbox、lxc等），transport
是选择该连接所使用的传输方式（可以为空，也可以是“unix”这样的值），path是连接到
服务器端上的某个路径，？extral-param是可以额外添加的一些参数（如Unix domain
sockect的路径）。
在libvirt中KVM使用QEMU驱动。QEMU驱动是一个多实例的驱动，它提供了一个系
统范围内的特权驱动（即“system”实例）和一个用户相关的非特权驱动（即“session”实
例）。通过“qemu：///session”这样的URI可以连接到一个libvirtd非特权实例，但是这个实
例必须是与本地客户端的当前用户和用户组相同的实例，也就说，根据客户端的当前用户
和用户组去服务器端寻找对应用户下的实例。在建立session连接后，可以查询和控制的域
或其他资源都仅仅是在当前用户权限范围内的，而不是整个节点上的全部域或其他资源。
而使用“qemu：///system”这样的URI连接到libvirtd实例，是需要系统特权账号“root”权限
的。在建立system连接后，由于它是具有最大权限的，因此可以查询和控制整个节点范围
内的域，还可以管理该节点上特权用户才能管理的块设备、PCI设备、USB设备、网络设
备等系统资源。一般来说，为了方便管理，在公司内网范围内建立到system实例的连接进
行管理的情况比较常见，当然为了安全考虑，赋予不同用户不同的权限就可以使用建立到
session实例的连接。
在libvirt中，本地连接QEMU/KVM的几个URI示例如下：
·qemu：///session：连接到本地的session实例，该连接仅能管理当前用户的虚拟化资
源。
·qemu+unix：///session：以Unix domain sockect的方式连接到本地的session实例，该连
接仅能管理当前用户的虚拟化资源。
·qemu：///system：连接到本地的system实例，该连接可以管理当前节点的所有特权用
户可以管理的虚拟化资源。
·qemu+unix：///system：以Unix domain sockect的方式连接到本地的system实例，该连
接可以管理当前节点的所有特权用户可以管理的虚拟化资源。
2.远程URI
除了本地管理，libvirt还提供了非常方便的远程的虚拟化管理功能。libvirt可以使用远
程URI来建立到网络上的Hypervisor的连接。远程URI和本地URI是类似的，只是会增加用
户名、主机名（或IP地址）和连接端口来连接到远程的节点。远程URI的一般格式如下：
driver[+transport]://[user@][host][:port]/[path][?extral-param]
其中，transport表示传输方式，其取值可以是ssh、tcp、libssh2等；user表示连接远程
主机使用的用户名，host表示远程主机的主机名或IP地址，port表示连接远程主机的端
口。其余参数的意义与本地URI中介绍的完全一样。
在远程URI连接中，也存在使用system实例和session实例两种方式，这二者的区别和
用途，与本地URI中介绍的内容是完全一样的。
在libvirt中，远程连接QEMU/KVM的URI示例如下：
·qemu+ssh：//root@example.com/system：通过ssh通道连接到远程节点的system实例，
具有最大的权限来管理远程节点上的虚拟化资源。建立该远程连接时，需要经过ssh的用
户名和密码验证或者基于密钥的验证。
·qemu+ssh：//user@example.com/session：通过ssh通道连接到远程节点的使用user用
户的session实例，该连接仅能对user用户的虚拟化资源进行管理，建立连接时同样需要经
过ssh的验证。
·qemu：//example.com/system：通过建立加密的TLS连接与远程节点的system实例相
连接，具有对该节点的特权管理权限。在建立该远程连接时，一般需要经过TLS x509安
全协议的证书验证。
·qemu+tcp：//example.com/system：通过建立非加密的普通TCP连接与远程节点的
system实例相连接，具有对该节点的特权管理权限。在建立该远程连接时，一般需要经过
SASL/Kerberos认证授权。
3.使用URI建立到Hypervisor的连接
在某个节点启动libvirtd后，一般在客户端都可以通过ssh方式连接到该节点。而TLS和
TCP等连接方式却不一定都处于开启可用状态，如RHEL 7.3系统中的libvirtd服务在启动时
就默认没有打开TLS和TCP这两种连接方式。关于libvirtd的配置可以参考4.1.2节中的介
绍。而在服务器端的libvirtd打开了TLS和TCP连接方式，也需要一些认证方面的配置，当
然也可直接关闭认证功能（这样不安全），可以参考libvirtd.conf配置文件。
我们看到，URI这个标识还是比较复杂的，特别是在管理很多远程节点时，需要使用
很多的URI连接。为了简化系统管理的复杂程度，可以在客户端的libvirt配置文件中为URI
命名别名，以方便记忆，这在4.1.2节中已经介绍过了。
在4.1.4节中已经介绍过，libvirt使用virConnectOpen函数来建立到Hypervisor的连接，
所以virConnectOpen函数就需要一个URI作为参数。而当传递给virConnectOpen的URI为空
值（NULL）时，libvirt会依次根据如下3条规则去决定使用哪一个URI。
1）试图使用LIBVIRT_DEFAULT_URI这个环境变量。
2）试用使用客户端的libvirt配置文件中的uri_default参数的值。
3）依次尝试用每个Hypervisor的驱动去建立连接，直到能正常建立连接后即停止尝
试。
当然，如果这3条规则都不能够让客户端libvirt建立到Hypervisor的连接，就会报出建
立连接失败的错误信息（“failed to connect to the hypervisor”）。
在使用virsh这个libvirt客户端工具时，可以用“-c”或“--connect”选项来指定建立到某个
URI的连接。只有连接建立之后，才能够操作。使用virsh连接到本地和远程的Hypervisor
的示例如下：
[root@kvm-host ~]# virsh -c qemu:///system
Welcome to virsh, the virtualization interactive terminal.
virsh # list
Id Name State
----------------------------------------------------
1 rhel7u1-1 running
2 rhel7u2-2 running
virsh # quit
[root@kvm-host ~]# virsh -c qemu+ssh://root@192.168.158.31/system
root@192.168.158.31's password:
Welcome to virsh, the virtualization interactive terminal.
Type: 'help' for help with commands
'quit' to quit
virsh # list
Id Name State
----------------------------------------------------
1 rhel7u2-remote running
virsh # quit
其实，除了针对QEMU、Xen、LXC等真实Hypervisor的驱动之外，libvirt自身还提供
了一个名叫“test”的傀儡Hypervisor及其驱动程序。test Hypervisor是在libvirt中仅仅用于测
试和命令学习的目的，因为在本地的和远程的Hypervisor都连接不上（或无权限连接）
时，test这个Hypervisor却一直都会处于可用状态。使用virsh连接到test Hypervisor的示例
操作如下：
[root@kvm-host ~]# virsh -c test:///default list
Id Name State
----------------------------------------------------
1 test running
[root@kvm-host ~]# virsh -c test:///default
Welcome to virsh, the virtualization interactive terminal.
Type: 'help' for help with commands
'quit' to quit
virsh # list
Id Name State
----------------------------------------------------
1 test running
virsh # quit
[1] 关于VMware的API、驱动和libvirt客户端连接VMWare的介绍，可以参考：
http://libvirt.org/drvesx.html。
[2] URI是一个字符序列，它用于唯一标识Web上抽象的或物理的资源。读者比较熟悉的
在浏览器中输入的URL就属于URI中的一种表现形式。URI包括统一资源名称（URN）和
统一资源定位器（URL）。关于URI的语法标准，可以参考RFC3986规范文档：
http://www.ietf.org/rfc/rfc3986.txt。
4.1.6　libvirt API使用示例
经过前面几节对libvirt的配置、编译、API、建立连接等内容的介绍，相信大家对
libvirt已经有了大致的了解。学习API的最好方法就是通过代码来调用API实现几个小功
能，所以本节主要通过两个示例来分别演示如何调用libvirt的由C语言和Python语言绑定的
API。
1.libvirt的C API的使用
在使用libvirt API之前，必须要在远程或本地的节点上启动libvirtd守护进程。在使用
libvirt的客户端前，先安装libvirt-devel软件包。本次示例中安装的是RHEL 7.3自带的
libvirt-devel软件包，如下：
[root@kvm-host ~]# rpm -q libvirt-devel
libvirt-devel-2.0.0-4.el7.x86_64
如下一个简单的C程序（文件名为dominfo.c）就是通过调用libvirt的API来查询一些关
于某个域的信息。该示例程序比较简单易懂，它仅仅是使用libvirt API的一个演示程序，
这里不做过多的介绍。不过，这里有三点需要注意：
1）需要在示例代码的开头引入<libvirt/libvirt.h>这个头文件；
2）由于只是实现查询信息的功能，所以可以使用virConnectOpenReadOnly来建立只
读连接；
3）这里使用了空值（NULL）作为URI，是让libvirt自动根据4.1.5节中介绍的默认规
则去建立到Hypervisor的连接。这里由于本地已经运行了libvirtd守护进程，并启动了两个
QEMU/KVM客户机，所以它默认会建立到QEMU/KVM的连接。
/**
* Get domain information via libvirt C API.
* Tested with libvirt-devel-2.0.0 on a RHEL 7.3 host system.
*/
#include <stdio.h>
#include <libvirt/libvirt.h>
int getDomainInfo(int id) {
virConnectPtr conn = NULL; /* the hypervisor connection */
virDomainPtr dom = NULL; /* the domain being checked */
virDomainInfo info; /* the information being fetched */
/* NULL means connect to local QEMU/KVM hypervisor */
conn = virConnectOpenReadOnly(NULL);
if (conn == NULL) {
fprintf(stderr, "Failed to connect to hypervisor\n");
return 1;
}
/* Find the domain by its ID */
dom = virDomainLookupByID(conn, id);
if (dom == NULL) {
fprintf(stderr, "Failed to find Domain %d\n", id);
virConnectClose(conn);
return 1;
}
/* Get virDomainInfo structure of the domain */
if (virDomainGetInfo(dom, &info) < 0) {
fprintf(stderr, "Failed to get information for Domain %d\n", id);
virDomainFree(dom);
virConnectClose(conn);
return 1;
}
/* Print some info of the domain */
printf("Domain ID: %d\n", id);
printf(" vCPUs: %d\n", info.nrVirtCpu);
printf(" maxMem: %d KB\n", info.maxMem);
printf(" memory: %d KB\n", info.memory);
if (dom != NULL)
virDomainFree(dom);
if (conn != NULL)
virConnectClose(conn);
return 0;
}
int main(int argc, char **argv)
{
int dom_id = 3;
printf("-----Get domain info by ID via libvirt C API -----\n");
getDomainInfo(dom_id);
return 0;
}
在获得dominfo.c这个示例程序之后，用virsh命令查看当前节点中的情况，再编译和
运行这个示例程序去查询一些域的信息。将二者得到的一些信息进行对比，可以发现得到
的信息是匹配的。命令行操作如下：
[root@kvm-host kvm_demo]# virsh list
Id Name State
----------------------------------------------------
3 kvm-guest running
[root@kvm-host kvm_demo]# virsh dommemstat 3
actual 1048576
rss 680228
[root@kvm-host kvm_demo]# virsh vcpucount 3
maximum config 2
maximum live 2
current config 2
current live 2
[root@kvm-host kvm_demo]# gcc dominfo.c -o dominfo -lvirt
[root@kvm-host kvm_demo]# ./dominfo
-----Get domain info by ID via libvirt C API -----
Domain ID: 3
vCPUs: 2
maxMem: 1048576 KB
memory: 1048576 KB
这里需要注意的是，在使用GCC编译dominfo.c这个示例程序时，加上了“-lvirt”这个
参数来指定程序链接时依赖的库文件，如果不指定libvirt相关的共享库，则会发生链接时
错误。在本次示例的RHEL 7.3系统中，需要依赖的libvirt共享库文件
是/usr/lib64/libvirt.so，如下：
[root@kvm-host ~]# ls /usr/lib64/libvirt.so
/usr/lib64/libvirt.so
2.libvirt的Python API的使用
在4.1.1节中已经介绍过，许多种编程语言都提供了libvirt的绑定。Python作为一种在
Linux上比较流行的编程语言，也提供了libvirt API的绑定。在使用Python调用libvirt之前，
需要安装libvirt-python软件包，或者自行编译和安装libvirt及其Python API。
本次示例是基于RHEL 7.3系统自带的libvirt和libvirt-python软件包来进行的，对libvirtpython
及Python中的libvirt API文件的查询，命令行如下：
[root@kvm-host ~]# rpm -q libvirt-python
libvirt-python-2.0.0-2.el7.x86_64
[root@kvm-host ~]# ls /usr/lib64/python2.7/site-packages/libvirt*
/usr/lib64/python2.7/site-packages/libvirt_lxc.py /usr/lib64/python2.7/site-packages/libvirt.py
/usr/lib64/python2.7/site-packages/libvirt_lxc.pyc /usr/lib64/python2.7/site-packages/libvirt.pyc
/usr/lib64/python2.7/site-packages/libvirt_lxc.pyo /usr/lib64/python2.7/site-packages/libvirt.pyo
/usr/lib64/python2.7/site-packages/libvirtmod_lxc.so /usr/lib64/python2.7/site-packages/libvirt_qemu.py
/usr/lib64/python2.7/site-packages/libvirtmod_qemu.so /usr/lib64/python2.7/site-packages/libvirt_qemu.pyc
/usr/lib64/python2.7/site-packages/libvirtmod.so /usr/lib64/python2.7/site-packages/libvirt_qemu.pyo
如下是本次示例使用的一个Python小程序（libvirt-test.py），用于通过调用libvirt的
Python API来查询域的一些信息。该Python程序示例的源代码如下：
#!/usr/bin/python
# Get domain info via libvirt python API.
# Tested with python2.7 and libvirt-python-2.0.0 on a KVM host.
import libvirt
import sys
def createConnection():
conn = libvirt.openReadOnly(None)
if conn == None:
print 'Failed to open connection to QEMU/KVM'
sys.exit(1)
else:
print '-----Connection is created successfully-----'
return conn
def closeConnnection(conn):
print ''
try:
conn.close()
except:
print 'Failed to close the connection'
return 1
print 'Connection is closed'
def getDomInfoByName(conn, name):
print ''
print '----------- get domain info by name ----------"'
try:
myDom = conn.lookupByName(name)
except:
print 'Failed to find the domain with name "%s"' % name
return 1
print "Dom id: %d name: %s" % (myDom.ID(), myDom.name())
print "Dom state: %s" % myDom.state(0)
print "Dom info: %s" % myDom.info()
print "memory: %d MB" % (myDom.maxMemory()/1024)
print "memory status: %s" % myDom.memoryStats()
print "vCPUs: %d" % myDom.maxVcpus()
def getDomInfoByID(conn, id):
print ''
print '----------- get domain info by ID ----------"'
try:
myDom = conn.lookupByID(id)
except:
print 'Failed to find the domain with ID "%d"' % id
return 1
print "Domain id is %d ; Name is %s" % (myDom.ID(), myDom.name())
if __name__ == '__main__':
name1 = "kvm-guest"
name2 = "notExist"
id1 = 3
id2 = 9999
print "---Get domain info via libvirt python API---"
conn = createConnection()
getDomInfoByName(conn, name1)
getDomInfoByName(conn, name2)
getDomInfoByID(conn, id1)
getDomInfoByID(conn, id2)
closeConnnection(conn)
该示例程序比较简单，只是简单地调用libvirt Python API获取一些信息。这里唯一需
要注意的是“import libvirt”语句引入了libvirt.py这个API文件，然后才能够使用
libvirt.openReadOnly、conn.lookupByName等libvirt中的方法。在本次示例中，必须被引入
的libvirt.py这个API文件的绝对路径是/usr/lib64/python2.7/site-packages/libvirt.py，它实际
调用的是/usr/lib64/python2.7/site-packages/libvirtmod.so这个共享库文件。
在获得该示例Python程序后，运



行该程序（libvirt-test.py），查看其运行结果，命令
行操作如下：
[root@kvm-host kvm_demo]# python libvirt-test.py 2>/dev/null
---Get domain info via libvirt python API---
-----Connection is created successfully-----
----------- get domain info by name ----------"
Dom id: 3 name: kvm-guest
Dom state: [1, 1]
Dom info: [1, 1048576L, 1048576L, 2, 257070000000L]
memory: 1024 MB
memory status: {'actual': 1048576L, 'rss': 680228L}
vCPUs: 2
----------- get domain info by name ----------"
Failed to find the domain with name "notExist"
----------- get domain info by ID ----------"
Domain id is 3 ; Name is kvm-guest

----------- get domain info by ID ----------"
Failed to find the domain with ID "9999"
Connection is closed





























# 第5章　KVM核心基础功能

KVM采用的是完全虚拟化（Full Virtualizaiton）技术，在KVM环境中运行的客户机（Guest）操作系统是未经过修改的普通操作系统。在硬件虚拟化技术的支持下，内核的KVM模块与QEMU的设备模拟协同工作，从而构成了一整套与物理计算机系统完全一致的虚拟化的计算机软硬件系统。

要运行一个完整的计算机系统，必不可少的也是最重要的子系统包括：处理器（CPU）、内存（Memory）、存储（Storage）、网络（Network）、显示（Display）等。本章将介绍KVM环境中这些基本子系统的基本概念、原理、配置和实践。

## 5.1　硬件平台和软件版本说明

**qemu命令行开启KVM加速功能**
需要在qemu启动的命令行加上“-enable-kvm”这个参数来使用KVM硬件加速功能。另外，如果已经安装了支持KVM的Linux发行版，则不一定需要自己重新编译内核（包括KVM模块）和用户态程序QEMU。如果已经安装了RHEL 7.3系统且选择了其中的虚拟化组件，则只需检查当前内核是否支持KVM（查看/boot/config-xx文件中的KVM相关配置，默认是打开的），以及kvm和kvm_intel模块是否正确加载（命令为lsmod|grepkvm）。然后找到qemu-kvm的命令行工具（通常位于/usr/libexec/qemu-kvm），就用这个qemu-kvm命令行工具来进行后面的具体实践，以便了解KVM，将本书中使用“qemusystem-x86_64”命令的地方替换为系统中实际的qemu-kvm的路径即可。关于qemu命令行参数基本都是一致的，不需要做特别的改变，如果遇到参数错误的提示，可查阅当前版本
的QEMU帮助手册。

## 5.2　CPU配置

### 5.2.1　vCPU的概念

QEMU/KVM为客户机提供一套完整的硬件系统环境，在客户机看来，其所拥有的CPU即是**vCPU**（virtual CPU）。在KVM环境中，每个客户机都是一个标准的Linux进程（QEMU进程），而每一个vCPU在宿主机中是QEMU进程派生的一个普通线程。

**vCPU在3种执行模式下的不同分工如下：**

（1）用户模式（User Mode）
主要处理I/O的模拟和管理，由QEMU的代码实现。
（2）内核模式（Kernel Mode）
主要处理特别需要高性能和安全相关的指令，如处理客户模式到内核模式的转换，处理客户模式下的I/O指令或其他特权指令引起的退出（VM-Exit），处理影子内存管理（shadow MMU）。
（3）客户模式（Guest Mode）
主要执行Guest中的大部分指令，I/O和一些特权指令除外（它们会引起VM-Exit，被Hypervisor截获并模拟）。、

vCPU在KVM中的这3种执行模式下的转换如图5-1所示。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图5-1　vCPU在KVM中的3种执行模式的转换.jpg)

在KVM环境中，整个系统的基本分层架构如图5-2所示。
在系统的底层CPU硬件中需要有硬件辅助虚拟化技术的支持（Intel VT或AMD-V等），宿主机就运行在硬件之上，KVM的内核部分是作为可动态加载内核模块运行在宿主机中的，其中一个模块是与硬件平台无关的实现虚拟化核心基础架构的kvm模块，另一个是硬件平台相关的kvm_intel（或kvm_amd）模块。而KVM中的一个客户机是作为一个用户空间进程（qemu）运行的，它和其他普通的用户空间进程（如gnome、kde、firefox、chrome等）一样由内核来调度，使其运行在物理CPU上，不过它由kvm模块的控制，可以在前面介绍的3种执行模式下运行。多个客户机就是宿主机中的多个QEMU进程，而一个客户机的多个vCPU就是一个QEMU进程中的多个线程。和普通操作系统一样，在客户机系统中，同样分别运行着客户机的内核和客户机的用户空间应用程序。

![](C:\Users\ELXXGWX\Desktop\my file\openstack\kvm-zimo.com总结\kvm实践\图5-2　KVM系统的分层架构.jpg)



### 5.2.2　SMP的支持

下面的Bash脚本（cpu-info.sh）可以根据/proc/cpuinfo文件来检查当前系统中的CPU数量、多核及超线程的使用情况。

```
#!/bin/bash
#filename: cpu-info.sh
#this script only works in a Linux system which has one or more identical physical CPU(s).
echo -n "logical CPU number in total: "
#逻辑CPU个数
cat /proc/cpuinfo | grep "processor" | wc -l
#有些系统没有多核也没有打开超线程，就直接退出脚本
cat /proc/cpuinfo | grep -qi "core id"
if [ $? -ne 0 ]; then
echo "Warning. No multi-core or hyper-threading is enabled."
exit 0;
fi
echo -n "physical CPU number in total: "
#物理CPU个数
cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l
echo -n "core number in a physical CPU: "
#每个物理CPU上core的个数(未计入超线程)
core_per_phy_cpu=$(cat /proc/cpuinfo | grep "core id" | sort | uniq | wc -l)
echo $core_per_phy_cpu
echo -n "logical CPU number in a physical CPU: "
#每个物理CPU中逻辑CPU(可能是core、threads或both)的个数
logical_cpu_per_phy_cpu=$(cat /proc/cpuinfo | grep "siblings" | sort | uniq | awk- F: '{print $2}')
echo $logical_cpu_per_phy_cpu
#是否打开超线程，以及每个core上的超线程数目
#如果在同一个物理CPU上的两个逻辑CPU具有相同的”core id”，那么超线程是打开的
#此处根据前面计算的core_per_phy_cpu和logical_core_per_phy_cpu的比较来查看超线程
if [ $logical_cpu_per_phy_cpu -gt $core_per_phy_cpu ]; then
echo "Hyper threading is enabled. Each core has $(expr $logical_cpu_per_phy_cpu / $core_per_phy_cpu ) threads."
elif [ $logical_cpu_per_phy_cpu -eq $core_per_phy_cpu ]; then
echo "Hyper threading is NOT enabled."
else
echo "Error. There's something wrong."
fi
```

  SMP（SymmetricMulti-Processor，对称多处理器）系统

SMP是如此的普及和被广泛使用，而QEMU在给客户机模拟CPU时，也可以提供对SMP架构的模拟，让客户机运行在SMP系统中，充分利用物理硬件的SMP并行处理优势。由于每个vCPU在宿主机中都是一个线程，并且宿主机Linux系统是支持多任务处理的，因此可以通过两种操作来实现客户机的SMP，一是将不同的vCPU的进程交换执行（分时调度，即使物理硬件非SMP，也可以为客户机模拟出SMP系统环境），二是将在物理SMP硬件系统上同时执行多个vCPU的进程。

在qemu命令行中，“-smp”参数即是配置客户机的SMP系统，其具体参数如下：

```
-smp [cpus=]n[,maxcpus=cpus][,cores=cores][,threads=threads][,sockets=sockets]
```

其中：
·n用于设置客户机中使用的逻辑CPU数量（默认值是1）。
·maxcpus用于设置客户机中最大可能被使用的CPU数量，包括启动时处于下线（offline）状态的CPU数量（可用于热插拔hot-plug加入CPU，但不能超过maxcpus这个上限）。
·cores用于设置每个CPU的core数量（默认值是1）。
·threads用于设置每个core上的线程数（默认值是1）。
·sockets用于设置客户机中看到的总的CPU socket数量。

下面通过KVM中的几个qemu命令行示例，来看一下如何将SMP应用于客户机中。

1

qemu-system-x86_64 -m 1G rhel7.img

不加smp参数，使用其默认值1，在客户机中查看CPU情况

2

qemu-system-x86_64 -smp 8 -m 8G rhel7.img

“-smp 8”表示分配了8个虚拟的CPU给客户机，在客户机中用前面提到的“cpuinfo.
sh”脚本查看CPU情况

3

qemu-system-x86_64 -m 8G -smp 8,sockets=2,cores=2,threads=2 rhel7.img

通过-smp参数详细定义了客户机中SMP的架构



qemu-system-x86_64 -m 8G -smp 4,maxcpus=8 rhel7.img -enable-kvm

通过-smp参数详细定义了客户机中最多有8个CPU可用，在系统启动之时有4个处于开
启状态





### 5.2.3　CPU过载使用

​	CPU的过载使用是让一个或多个客户机使用vCPU的总数量超过实际拥有的物理CPU数量。QEMU会启动更多的线程来为客户机提供服务，这些线程也被Linux内核调度运行在物理CPU硬件上。

​        关于CPU的过载使用，推荐的做法是对多个单CPU的客户机使用over-commit

​	关于CPU的过载使用，最不推荐的做法是让某一个客户机的vCPU数量超过物理系统上存在的CPU数量。

​	总的来说，KVM允许CPU的过载使用，但是并不推荐在实际的生产环境（特别是负载较重的环境）中过载使用CPU。在生产环境中过载使用CPU，有必要在部署前进行严格的性能和稳定性测试。

​	利用客户机使用物理CPU时间差异，保证物理CPU一直处在最大状态，如果8核物理机，开3个客户机都是8核的，但3个客户机运行的时间不一样，一个早上，一个下午，一个晚上。

5.2.4　CPU模型

​      qemu64,kvm64,等

​      好处：便于迁移，兼容等问题

4.2.5　进程的处理器亲和性和vCPU的绑定（**）

​      一个进程在前一个时间片是在CPUM上，但是在后一个时间片是在CPUN上，

​      亲和性是指：将进程绑定到指定的一个或多个CPU上，而不允许将进程调度到其他进程上。

​      每个vCPU是宿主机上的一个普通的Qemu进程，使用taskset工具，设置处理器的亲和性，将某个vCPU绑定到某个或几个固定的cpu上去调度。

​      测试步骤：

​        1）启动宿主机时，在linux内核上加上“isolcpus="参数，实现cpu的隔离，从宿主机中隔离出几个cpu供客户机使用；

​        2）启动2个客户机，并实现vcpu和物理cpu的绑定。



4.3　内存配置
4.3.1　内存设置基本参数

​    1)qemu-system-x86_64 rhe16u3.img

​    2)客户机中，free -m  ,查看内核使用的情况

​                         dmesg


4.3.2　EPT和VPID简介

​    客户机虚拟地址GVA——>客户机物理地址GPA转换，通过客户机操作系统实现

​    客户机物理地址GPA——>宿主机物理地址HPA转换，通过Hypervisor实现

   

​    影子页表，软件实现GVA——>HPA的转换过程，后来引入EPT，硬件实现GVA——GPA——HPA的转换。

​    VPID，虚拟处理器标识，在硬件上为每个TLB项增加一个标识，用于区分不同的虚拟处理器的地址空间。

4.3.3　大页（Huge Page）

​    4KB的内存页——>2MB的内存页，减少了内存页的数量，提高了缓存命中率，这是一种提高性能的技术手段。
4.3.4　内存过载使用

​    内存不足，解决方案

​    1）内存交换，和交换分区来交换，openstack目测使用的就是这种方式。

​            性能较差，要求（物理内存空间+交换空间大小总和）>所有客户机的内存总和。

​            举例：64个内存1G的客户机，32G内存的物理机，如何分区，其中宿主机维持自身进程占用资源4G。

​                   客户机要求的交换分区总和   64x1G+4G-32G=36G.

​                   安装redhat建议，32G的物理内存，建议使用8G的交换分区。

​                   故而，在宿主机中使用 44GB(36GB+8GB)的交换分区来满足安全使用内存过载问题。

​    2）气球（ballooning技术），通过virio_balloon驱动来实现宿主机和客户机之间的协作。网易的openstack实践中好像就是用这种。

​    3）页共享（page sharing），通过KSM合并多个客户机进程使用相同的内存页。
4.4　存储配置
4.4.1　存储配置和启动顺序



​         1）qumu-kvm参数      -hda file    /  -hdb file  / ... /  -fdb  file  ； -driver参数

​         2）客户机的启动顺序：即类似Bios中系统引导顺序

​         3）举例

4.4.2　qemu-img命令

​        1）qemu-img check rhe16.img 检查镜像文件；

​        2）qemu-img create -f qcow2 -o ? temp.cow

​        3)  qemu-img convertmy -o qcow2 rhe16.img rhe16-1.gcow2

​        4)  qemu-img info rhe16.img

​        5)  snapshot  /rebase /resize  
4.4.3　QEMU支持的镜像文件格式

​        1)raw——原始格式，一次性占用磁盘空间。

​        2）qcow2——支持稀疏文件和加密、压缩。qcow——老版本，支持后端镜像和加密

​        3）sheepdog——为KVM虚拟化提供块存储，单点无故障，淘宝贡献较多。

​        4）clinder——openstack镜像块存储。

4.4.4　客户机存储方式

​        1）物理磁盘或磁盘分区；

​        2）LVM

​        3）分布式文件系统，NFS，iSCSI，GFS2



4.5　网络配置

​        1）QEMU支持的网络模式——virtio类型
​        A.使用网桥模式，通过linux-bridge来实现。此部分可以实际参考。

​        B.使用NAT模式——此部分可以参考，讲的不错。

​                dnsmasq，宿主机中运行的DHCP工具，给宿主机分配NAT内网的IP地址。基本架构图。

​                bridge-util 管理linux-brige的工具

​                iptables 对内核中IPv4包过滤工具和NAT管理工具。
​        C.QEMU内部的用户模式网络

​                Qeum自身实现的网络管理，性能差，不常用。
​        D.其他网络选项


4.6　图形显示
4.6.1　SDL的使用
4.6.2　VNC的使用
4.6.3　VNC显示中的鼠标偏移
4.6.4　非图形模式
4.6.5　显示相关的其他选项
4.7　本章小结
4.8　本章注释和参考阅读



------



第5章　KVM高级功能详解
5.1　半虚拟化驱动
5.1.1　virtio概述（Qemu模拟I/O设备的基本原理和优缺点，virtio的基本原理和优缺点
5.1.2　安装virtio驱动（Linux、Windows中virtion驱动程序的安装、使用）
5.1.3　使用virtio_balloon（1.ballooning简介；2.KVM中balloning的原理及优劣势；3.KVM中ballooning使用示例；4.通过ballooning过载使用内存）
5.1.4　使用virtio_net(半虚拟化网络设备--1.配置和使用；2.宿主机中的TSO和GSO设置；3.用vhost_net后端驱动）
5.1.5　使用virtio_blk（使用virtio API为客户机提供访问块设备的IO方法）
5.1.6　kvm_clock配置（半虚拟化时钟，为客户机提供精准的System time和Wall time）
5.2　设备直接分配（VT-d）
5.2.1　VT-d概述

​     Emulated device: QEMU纯软件模拟的设备

​     Virtio device：实现virtio API的半虚拟化驱动的设备

​     PCI device assignment：PCI设备直接分配（VT-d)

5.2.2　VT-d环境配置

​     （1.硬件支持和BIOS设置；2.宿主机内核的配置；3.在宿主机中隐藏设备；4.通过Qemu命令行分配设备给客户机)
5.2.3　VT-d操作示例

​      (1.网卡直接分配；2.硬盘直接分配；3.USB直接配置；4.VGA显卡直接分配）
5.2.4　SR-IOV技术——多个虚拟机共享一个物理设备资源，达到设备直接分配的性能。

​      （1.SR-IOV概述，物理功能，虚拟功能）

​      （2.SR-IOV操作示例）

​      （3.SR-IOV使用问题解析）


5.3　热插拔——电脑运行时（不关闭电源）插上或拔除硬件
5.3.1　PCI设备热插拔
5.3.2　PCI设备热插拔示例（1.网卡的热插拔；2.USB的热插拔；3.SATA硬盘的热插拔）
5.3.3　CPU和内存的热插拔


5.4　动态迁移
5.4.1　动态迁移的概念

​      （迁移概念，静态迁移，动态迁移。）
5.4.2　动态迁移的效率和应用场景

​       (衡量条件：整体迁移时间，服务器停机时间，对服务器性能的影响）
5.4.3　KVM动态迁移原理和实践

​       （先迁移内存、后迁移配置；KVM动态迁移应该注意的事项，在KVM上具体进行的操作步骤）
5.4.4　VT-d/SR-IOV的动态迁移




5.5　嵌套虚拟化
5.5.1　嵌套虚拟化的基本概念（Xen On Xen和KVM On Xen，VMware on VMware 和KVM on KVM等等）
5.5.2　KVM嵌套KVM（主要步骤）


5.6　KSM技术—写实复制。
5.6.1　KSM基本原理—内核同页合并。

​    KSM允许内核在两个或多个进程（包括虚拟机客户机）之间共享完全相同的内存页。
5.6.2　KSM操作实践

​    配置文件
5.7　KVM其他特性简介
​    5.7.1　1GB大页

​       （2MB->1GB,减少内存页表数量，提高TLB缓存的效率，从而提高了系统的内存访问性能。

​         1GB大页的使用步骤）
​    5.7.2　透明大页

​        （提高系统内存的使用效率和性能。

​          使用透明大页的步骤）

5.7.3　AVX和XSAVE——高级矢量扩展。
5.7.4　AES新指令——指令的配置、测试
5.7.5　完全暴露宿主机CPU特性——CPU模型特性、CPU信息查看。
5.8　KVM安全
5.8.1　SMEP—安全渗透，监督模式执行保护
5.8.2　控制客户机的资源使用-cgroups—linux内核中的一个特性，用于限制、记录和隔离进程组对系统物理资源的使用。

​       cgroups的功能—资源限制，优先级控制，记录，隔离，控制。

​       cgroups子系统。

​       cgroups操作示例：通过cgroups的blkio子系统来设置2个客户机对磁盘I/O读写的优先级。
5.8.3　SELinux和sVirt

​       SELinux—linux内核中的安全访问体系（MAC，强制访问控制模式），为每一个应用程序提供一个“沙箱”，只允许应用程序执行它设计需要的且在安全策略中明确允许的任务，对每个应用程序只分配它正常工作所需要的对应权限。

​       sVirt—对虚拟化客户机使用强制访问控制来提高安全性，阻止因为Hypervisor的bug而导致的从一台客户机向宿主机或其他服务器的攻击。

​       SELinux和sVirt的配置和操作示例。
5.8.4　可信任启动-Tboot

​       TXT—在PC或服务器系统启动是对系统关键部位进行验证的硬件解决方案。

​       TBoot—可信启动，是使用TXT技术在内核或Hypervisor启动之前的一个软件模块，用于度量和验证操作系统或Hypervisor的启动过程。

​       使用TBoot的示例。
5.8.5　其他安全策略

​       1.镜像文件加密

​       2.虚拟网络的安全

​       3.远程管理的安全

​       4.普通Linux系统的安全准则


5.9　QEMU监控器
5.9.1　QEMU monitor的切换和配置

5.9.2　常用命令介绍

​      help，info,info version ,info ,commit,cont,change,balloon,cup index,log,sendkey keys,x和xp，p或print fmt expt
5.10　qemu-kvm命令行参数

​      qemu-system-x86_64[options] [disk_images]

​      cpu的相关参数—-cpu参数，-smp参数

​      磁盘相关的参数

​      网络相关的参数

​      图形显示相关的参数

​      Vt-d和SR-IOV相关参数

​      动态迁移的参数

​      已用过的其他参数
5.10.1　回顾已用过的参数
5.10.2　其他常用参数


5.11　迁移到KVM虚拟化环境
5.11.1　virt-v2v工具介绍—将虚拟客户机从一些Hypervisor（也包括KVM自身）迁移到KVM环境中去。
5.11.2　从Xen迁移到KVM

​      virt-v2v-ic xen+ssh://[root@xen0.demo.com](mailto:root@xen0.demo.com) -os pool -b brnamevm-name
5.11.3　从VMware迁移到KVM

​      virt-v2v-ic esx://esx.demo.com/ -os pool --bridege brame vm-name
5.11.4　从VirtualBox迁移到KVM

​      virt-v2v -ic vbox+ssh://[root@vbox.demo.com](mailto:root@vbox.demo.com) -os pool -b bramevm-name
5.11.5　从物理机迁移到KVM虚拟化环境（P2V）

​      
5.12　本章小结
5.13　注释和参考阅读





------




第6章　KVM管理工具
6.1　libvirt
6.1.1　libvirt简介

   对KVM虚拟机进行管理的工具和应用程序接口、守护进程和管理工具。

   libvirt目标、交互框架、支持的虚拟机、主要的功能、支持的语言、主要进程

6.1.2　libvirt的编译、安装和配置
6.1.3　libvirt和libvirtd的配置

  /etc/libvirt/libvirt.conf——用来配置一些常用libvirt连接（通常是远程连接的）别名

  /etc/libvirt/libvirtd.conf——libvirt的守护进程libvirtd的配置文件，是一些启动设置，包括打开TCP连接、设置TCP监听端口、TCP连接认证授权方式、设置UNIX domain的保存目录等。

  /etc/libvirt/qemu.conf——对Qeum的驱动的配置文件

  /etc/libvirt/qume/目录/——存放的是使用Qume驱动域的配置文件

  libvirtd——是libvirt虚拟化管理工具的服务器端的守护进程。（要让某个节点能够使用libvirt进行管理，都需要在这个节点上安装该守护进程） libvirt的客户端程序包括——virsh，virt-manager。

  libvirtd的常见命令行。
6.1.4　libvirt域的XML配置文件

​    Libvirt对虚拟机管理，实质是基于xml文件作为配置文件。

​    客户机的XML文件，其中CPU配置（vcpu、cpuset，vcpupin），内存的配置（memory），客户机系统类型及其启动顺序，网络的配置（桥接方式，NAT方式，用户模式网络的设置，网卡设备直接分配（VT-d),存储的配置，域的配置，QEMU模拟器的配置，图形显示的方式，客户机声卡和显卡的配置，PCI控制器

6.1.5　libvirt API简介

​    连接Hypervisor相关API：以virConnect开头的一系列操作，

​        连接函数 virConnectOpen,virConnectOpenReadOnly,virConncetOpenAuth

​        交互：virConectGetCapabilities,virConnectListDomains

​        关闭操作：virConnectClose

​    域管理的API：以virDomain开头的一系列函数

​        获取域对象：virDomainPtrvirDomainLookupByID，virDomainPtrvirDomainLookupByID

​        查询域信息，控制域的生命周期

​    节点管理的API：以virNode开头的一系列函数

​        获取各种资源信息：virNodeGetInof,virNodeGEtCPUStatus,virNodeGetMemoryStats，virNodeGetFreeMemory，virNodeSuspendForDuration

​    网络管理的API：以virNetwork开头的和virInterface开头的

​    存储卷管理的API：以virStorageVol开头的一系列函数

​    存储池管理的API：以virStroagePool开头的一系列函数

​    事件管理API：以virEvent开头的一系列函数

​    数据流管理的API：以virStream开头的一系列函数

6.1.6　建立到Hypervisor的连接

​    CS架构，服务器端运行Hypervisor，其上需要Libvirtd这个守护进程，科幻段连接到Libvirtd从而进行管理操作。

​    本地URI——客户端使用本地URL用于连接本系统范围内的Hypervisor；

​    远程URI

​    使用URI   virsh -c qemu:///system

​              virsh -c qemu+ssh://root@192.168.158.31/system



6.1.7　libvirt API使用示例

​     使用C API连接客户机，查询域信息

​     使用python API连接客户机，查询域信息


6.2　virsh

6.2.1　virsh简介

​      管理虚拟化环境中的客户机和Hypervisor的命令行工具，客户端连接程序。两种工作模式，交互模式和非交互模式。
6.2.2　virsh常用命令

​      域管理命令（list，dominfo,domid,....)

​      宿主机和Hypervisor的管理（version,sysinfo,nodeinfo,...)

​      网络管理命令（iface-list，iface-name，net-list,net-edit,...)

​      存储池和存储卷的管理命令（pool-list,pool-info<pool-name>,...)
6.3　virt-manager

6.3.1　virt-manager简介

​      管理虚拟机的图形化的桌面用户接口
6.3.2　virt-manager编译和安装

6.3.3　virt-manager使用

​      1.打开virt-manager

​      2.创建、启动、暂停、关闭一个客户机；

​      3.连接到本地和远程的Hypervisor

​      4.查看和修改客户机的详细配置

​      5.动态迁移

​      6.性能统计图像界面，可以统计客户机CPU利用率、客户机磁盘IO，客户机网络IO等

6.4　virt-viewer、virt-install和virt-top
6.4.1　virt-viewer——用于与虚拟化客户机的图形显示的轻量级的交行接口工具。
6.4.2　virt-install——为virt-manager的图形界面和创建客户机提供安装系统的API。
6.4.3　virt-top——用于展示虚拟化客户机状态和资源利用率的工具。


6.5　OpenStack云计算平台
6.5.1　OpenStack简介
6.5.2　使用DevStack安装和配置OpenStack开发环境
6.5.3　在OpenStack中使用KVM
6.6　本章小结
6.7　本章注释和参考阅读





------


第7章　Linux发行版中的KVM
7.1　RHEL和Fedora中的KVM
7.1.1　Red Hat、RHEL、Fedora和CentOS简介
7.1.2　RHEL中的KVM
7.1.3　Fedora中的KVM
7.2　SLES和openSUSE中的KVM
7.2.1　SLES中的KVM
7.2.2　openSUSE中的KVM
7.3　Ubuntu中的KVM
7.4　本章小结
7.5　本章注释和参考阅读





------


第8章　KVM性能测试及参考数据

虚拟化方案——功能和性能；功能是实现虚拟化的基础，性能是虚拟化效率的关键指标。评价一个系统的性能指标：

 响应时间：客户端发出请求到响应的整个过程所花费的时间

 吞吐量：指在一次性能测试过程中网络上传输的数据量的总和。

 并发用户数：指在使用一个系统服务的用户数量

 资源占用率：使用某个服务时，客户端和服务器占用资源的情况。

​     CPU密集型：科学计算；网络IO秘籍型：web服务；磁盘IO密集型：数据库服务；内存密集型：缓存服务



8.1　虚拟化性能测试简介


8.2　CPU性能测试
8.2.1　CPU性能测试工具

   SPECCPU2006

   SPECjbb2005:评估服务器端Java应用性能的基准测试程序

   UnixBench：类Unix系统提供的基础的衡量指标

   SysBench：系统在模拟高压力数据库应用中的性能

   PCMark：针对一个计算机系统整体及其部件进行性能评估的基准测试工具。

   内核编译：CPU密集型、也可是内存密集型

   Super PI：典型的计算CPU密集型基准测试工具。

8.2.2　测试环境配置

   宿主机、客户机软硬件环境，内核选项配置情况

8.2.3　性能测试方法

   SPEC CPU2006测试安装

   内核编译

   Super PI
8.2.4　性能测试数据


8.3　内存性能测试
8.3.1　内存性能测试工具

​     LMbench——评价系统综合性能的良好工具。

​     Memtest86++——内存检测工具

​     STREAM——衡量系统运行一些简单矢量计算内核是能达到的最大内存带宽和相应的计算速度。
8.3.2　测试环境配置
8.3.3　性能测试方法

​     LMbench——评估KVM内存虚拟机性能。会生成一个系统测试文档和测试结果报告
8.3.4　性能测试数据



8.4　网络性能测试
8.4.1　网络性能测试工具

​     Netperf——网络性能测试工具，可以测试多个方面。

​     Iperf——常用的网络测试工具

​     NETIO——使用不同大小的数据包来测试TCP和UDP网络连接的吞吐量。

​     SCP——最常用的远程文件复制工具。

8.4.2　测试环境配置

​     注意网卡配置，使用默认的rt181139模式的网桥网络、使用virtio-net（QEMU做后端驱动）的网桥网络，使用virtio-net模式的网桥网络，

​     VT-d直接分配PF，SR-IOV直接分配VF
8.4.3　性能测试方法

​     Netperf

​     SCP
8.4.4　性能测试数据

​     不同配置下的Netperf测试数据；不同配置下的SCP测试数据

​     结论：

​       配置对比：virtio、VT-d和SR-IOV模式，可以达到和原生系统网络差不多的性能；在达到相同带宽的情况下，VT-d和SR-IOV方式占用的CPU资源比virtio略少；纯软件模拟的rt181139和e1000网卡的性能较差。



8.5　磁盘I/O性能测试
8.5.1　磁盘I/O性能测试工具

  DD——文件复制工具；

  IOzone——通过对多种文件进行操作，来衡量一个文件系统的性能。

  Bonnie++——可以模拟数据库去访问一个单一的大文件

  hdparm——获取和设置SATA和IDE设备的参数工具，粗略的测试磁盘IO的性能。

8.5.2　测试环境配置

  使用纯软件模拟IDE磁盘和使用virtio-blk驱动的磁盘。
8.5.3　性能测试方法

  DD、IOZone、Bonnie++
8.5.4　性能测试数据
8.6　本章小结
8.7　本章注释和参考阅读





------

第9章　参与KVM开源社区

9.1　开源社区介绍
9.1.1　Linux开源社区

​     Linux内核代码维护层次结构
9.1.2　KVM开源社区

​     KVM Forum，http://www.linux-kvm.org/page/KVM_Forum
9.1.3　QEMU开源社区

​     Qume:  [http://git.qemu.org/](javascript:void())    
9.1.4　其他开源社区

​     Libvirt 一个虚拟化API项目   [www.libvirt.org](javascript:void())

​     OpenStack  [www.openstack.org](javascript:void())

​     CloudStack cloudstack.apache.org

​     Xen        [www.xen.org](javascript:void())

​     Apache     httpd.apache.org

​     Nginx      [www.nginx.org](javascript:void())

​     Hadoop     hadoop.apache.org 

9.2　代码结构简介
9.2.1　KVM代码   

​     kvm框架核心代码  位于目录 virt/kvm/下

​     与硬件架构相关的代码，位于  arch/*/kvm
9.2.2　QEMU代码

​     QEMU代码实现了对PC客户机的完全模拟。

​     QEMU配合KVM启动一个客户机的流程。先打开 /dev/kvm设备，通过名为 KVM_CREATE_VM的IOCTL调用来创建一个虚拟机对象，然后通过KVM_CREATE_VCPU为虚拟机创建vcpu对象，最后通过 KVM_RUN 让vCPU 运行起来。这个抽象后的简化过程如下：

​     main(): vl.c

​     configure_accelerator():vl.c -> kvm_init(): kvm_all.c

​     machine->init():vl.c            qemu_open("/dev/kvm"):kvm_all.c

​     pc_init_pci():pc_piix.c         kvm_ioctl(KVM_CREATE_VM):kvm_all.c

​     pc_init1():hw/i386/pc_piix.c

​     pc_nex_cpu():hw/i386/pc.c

​     ...

​     qemu_init_vcpu():cpu.c

​     qemu_kvm_start_vcpu():cpu.c

​     qemu_thread_create():util/qemu-thread-posix.c

​     pthread_create():#create vCPU thread

​     qume_kvm_cpu_thread_fn(): cpu.c

​     kvm_init_vcpu:kvm-all.c

​     kvm_vm_ioctl(KVM_CREATE_VCPU)



9.2.3　KVM单元测试代码

​     基本原理：将编译好的轻量级测试内核镜像（*.flat文件）作为支持多重启动的QEMU的客户机内核镜像来启动，测试使用一个通过客户机BIOS来调用的基础架构，该基础架构将会主要初始化客户机系统（包括CPU等），然后切换到长模式（x86_64 CPU架构的一种运行模式）并调用各个具体测试用例的主函数从而执行测试，在测试完成QEMU进程自动退出。

9.2.4　KVM Autotest代码

​     
9.3　向开源社区贡献代码
9.3.1　开发者邮件列表
9.3.2　代码风格

​     缩进；长的行和字符串打乱（每一行的长度不要超过80个词）；大括号的位置；空格的使用；
9.3.3　生成patch

​     patch：添加的新功能或者修复某个bug的代码。

​     使用diff工具或git工具可以生成patch

​      diff -urN kvm.git/ kvm-my.git/ >my.patch

​      git add virt/kvm/kvm_main.c
9.3.4　检查patch

​      使用脚步检查patch是否合规： scripts/checkpatch.pl

9.3.5　提交patch 9.4　提交KVM相关的bug 9.4.1　通过邮件列表提交bug 9.4.2　使用bug管理系统提交bug 9.4.3　使用二分法定位bug 9.5　本章小结 9.6　本章注释和参考阅读