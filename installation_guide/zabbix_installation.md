##########################################################################################

**zabbix架构**

![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/installation_guide/image_folder/zabbix_structure.jpg)
	
**zabbix进程**

![Image text](https://raw.githubusercontent.com/caspeerpoiuy/data-structures-and-algorithms-/master/installation_guide/image_folder/zabbix_process.png)	

	（1）报警功能
	（2）分布式功能
	（3）自动发现功能
	（4）监控功能
	（5）管理功能



##########################################################################################
**<h3>Installation procedure**

**a. Install Zabbix repository**
		
	# wget https://repo.zabbix.com/zabbix/4.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_4.2-1+xenial_all.deb
	# dpkg -i zabbix-release_4.2-1+xenial_all.deb
	# apt update
	
**b. Install Zabbix server, frontend, agent**

	# apt -y install zabbix-server-mysql zabbix-frontend-php zabbix-agent
	
**c. Create initial database**

	# mysql -uroot -p"casper"
	mysql> create database zabbix character set utf8 collate utf8_bin;
	mysql> grant all privileges on zabbix.* to root@localhost identified by 'casper';
	mysql> quit;
	
**d. Configure the database for Zabbix server**

	sudo vi /etc/zabbix/zabbix_server.conf
	modify DBPassword="casper"
	
**e. Configure PHP for Zabbix frontend**

	sudo vi /etc/zabbix/apache.con
	modify php_value date.timezone Europe/Riga
	
**f. Start Zabbix server and agent processes**

	# systemctl restart zabbix-server zabbix-agent apache2
	# systemctl enable zabbix-server zabbix-agent apache2
	