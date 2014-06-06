#encoding=utf-8
from initial_partitioning import *
sn = 16*1
traffic = [[1,0,2,0,3,0,3,0,1,0,1,0,4,0,1,0] for row in range(sn)]
link_latency = [[1 for col in range(sn)] for row in range(sn)]
s_wei = [3,2,4,2,2,5,2,2,2,2,1,1,1,1,1,1]
l_wei = traffic
partition = 0
def get_partition_graph(part_no):
	print 'partition_graph'
	index = []
	s_wei = []
	count = 0
	for i in range(len(partition)): 
		print '%d '%partition[i],
		if partition[i] == part_no:
			count += 1
			index.append(i)
			
	print ''
	print '%d: %d'%(part_no,count)
	print 'index:'
	for i in index:
		print '%d '%i,
	print ''
if __name__=='__main__':
	partition = initial_partition( s_wei, l_wei, 0, 1)
	pn = gv.level**2
	part = [0]*pn
	sw   = [0]*pn
	print 'switch weight'
	for i in range(sn):
		print '%2d '%s_wei[i],
	print ''
	print '交换机分区情况'
	for i in range(sn):
		part[partition[i]-pn] += 1
		sw[partition[i]-pn] += s_wei[i]
		print '%2d '%partition[i],
	print ''
	print '各个分区交换机数量'
	for i in range(pn):
		print '%2d '%part[i],
	print ''
	print '各个分区的交换机权重总和'
	for i in range(pn):
		print '%2d '%sw[i],
	print ''
	edge_cut = 0
	for i in range(sn-1):
		for j in range(i+1, sn):
			if partition[i] != partition[j]:
				edge_cut += l_wei[i][j]	
	print '割边数量：%d'%edge_cut
	for i in range(pn,pn*2):
		get_partition_graph(i)
