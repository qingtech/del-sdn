#coding:utf-8
#全局变量
#net_topo_file = 'net_topo.txt'
net_topo_file_name = 'null.txt' #网络拓扑矩阵文件名
net_traf_file_name = 'null.txt' #网络流量矩阵文件名
level = 0	#划分区域个数为2^level个,inital_partitioning.py使用该变量
c_num = 4	#controller number
s_num = 10	#switch number
l_num = 120	#link number
#net_topo = [[0 for col in range(5)] for row in range(3)];
net_topo = 1 #网络拓扑矩阵
net_traf = 1 #网络流量矩阵
#topo weight
c_wei = 1
s_wei = 1
l_wei = 1
if __name__ == '__main__':
	print 'hello, world'
