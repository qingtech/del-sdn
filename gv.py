#coding:utf-8
#全局变量
#net_topo_file = 'net_topo.txt'
net_topo_file = 'os3e.txt'
topo_wei_file = 'topo_wei.txt'
level = 2	#划分区域个数为2^level个,inital_partitioning.py使用该变量
c_num = 4	#controller number
s_num = 10	#switch number
l_num = 120	#link number
#net_topo = [[0 for col in range(5)] for row in range(3)];
net_topo = 1
#topo weight
c_wei = 1
s_wei = 1
l_wei = 1
if __name__ == '__main__':
	print 'hello, world'
