#encoding:utf-8
import gv
import sys
import error
import random
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'

#复杂度：O(switch_number)
def randomly_get_bipartition(s_wei, lc_part, rc_part):
	sum_wei = 0
	for sw in s_wei:
		sum_wei += sw
	sn = len(s_wei)
	partition = [0]*sn
	lsw = 0
	rsw = sum_wei
	while abs(rsw-lsw) > sum_wei*0.4:
		rsw = lsw = 0
		for i in range(sn):
			if random.randint(0,1) == 0:
				partition[i] = lc_part
				lsw += s_wei[i]
			else:
				partition[i] = rc_part
				rsw += s_wei[i]
	return partition

#index = [3,2,1,0]
#s_wei = [2,3,4,5]
#weight[s0] = 5, weight[s1] = 4, weight[s2] = 3, weight[s3] = 2
#设交换机数量为sn,则
#s_wei[sn]代表各个交换机的权重
#l_wei[sn][sn]代表链路权重
#level代表当传划分的层次,从第0层开始
#part代表当前分区
def initial_partition(s_wei,l_wei,level,part):
	#数据合法性检验
	if level < 0 or level > gv.level:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
		
	sn = len(s_wei)
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_wei) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_wei[i]) != sn:
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
		
	partition = [part]*sn
	#print 'partition.len=%d'%len(partition)
	#最后一层，无需再划分
	if level == gv.level:
		return partition
	#get bipartition of graph
	#获取两个子分区
	#         1
	#       /   \
	#     /       \
	#    2          3
	#  /  \       /   \
	# 4    5     6     7
	#/ \  / \   / \   / \
	#8 9 10 11 12 13 14 15
	lc_part = part*2	 #left  child part
	rc_part = part*2 + 1	 #right child part
	edge_cut = sys.maxint
	for i in range(1):
		partition = randomly_get_bipartition(s_wei, lc_part, rc_part)
		#print 'partition.len=%d'%len(partition)
		#微调左右partition
		tmp = 0
		for j in range(sn-1):
			for k in range(j,sn):
				if partition[j] != partition[k]:
					tmp += l_wei[j][k]
		if tmp < edge_cut:
			edge_cut = tmp
		

	#part 0 of bipartition
	#part 1 of bipartition
	#统计左右分区交换机个数
	sn0 = 0
	sn1 = 0
	for i in range(sn):
		if partition[i] == lc_part:
			sn0 +=1
		else:# if partition[i] == rc_part:
			sn1 +=1
	#print 'sn0=%d,sn1=%d'%(sn0,sn1)
	index_0 = [0]*sn0
	index_1 = [0]*sn1
	s_wei_0 = [0]*sn0
	s_wei_1 = [0]*sn1
	l_wei_0 = [[0]*sn0]*sn0
	l_wei_1 = [[0]*sn1]*sn1
	#index,s_wei
	i0 = 0
	i1 = 0
	for i in range(sn):
		if partition[i] == lc_part:
			index_0[i0] = i
			s_wei_0[i0] = s_wei[i]
			i0 += 1
		else:# if partition[i] == rc_part:
			index_1[i1] = i
			s_wei_1[i1] = s_wei[i]
			i1 += 1
	#复杂度：O(switch_number^2)
	#l_wei_0
	ii = 0
	#print 'sn0=%d,sn1=%d'%(sn0,sn1)
	for i in range(sn):
		if partition[i] == lc_part:
			#print 'ii=%d'%ii
			jj = 0
			for j in range(sn):
				if partition[j] == lc_part:
					l_wei_0[ii][jj] = l_wei[i][j]
					#print '%d '%jj
					jj += 1
			ii += 1	

	#l_wei_1
	ii = 0
	for i in range(sn):
		if partition[i] == rc_part:
			jj = 0	
			for j in range(sn):
				if partition[j] == rc_part:
					l_wei_1[ii][jj] = l_wei[i][j]
					jj += 1
			ii += 1	
	part_0 = initial_partition(s_wei_0,l_wei_0,level+1, lc_part)
	#print 'partition.len=%d,part_0.len=%d'%(len(partition),len(part_0))
	for i in range(sn0):
		#print 'i=%d,index_0[i]=%d'%(i,index_0[i])
		partition[index_0[i]] = part_0[i]
	part_1 = initial_partition(s_wei_1,l_wei_1,level+1, rc_part)
	for i in range(sn1):
		partition[index_1[i]] = part_1[i]
	return partition
if __name__ == '__main__':
	sn = 16*1
	#s_wei = [1]*sn
	s_wei = [20,20,20,2,2,2,2,2,2,2,1,1,1,1,1,1]
	l_wei = [[1,0,2,0,3,0,3,0,1,0,1,0,4,0,1,0]*1 for row in range(sn)]
	partition = initial_partition( s_wei, l_wei, 0, 1)
	pn = gv.level**2
	part = [0]*pn
	sw   = [0]*pn
	for i in range(sn):
		print '%2d '%s_wei[i],
	print ''
	for i in range(sn):
		part[partition[i]-pn] += 1
		sw[partition[i]-pn] += s_wei[i]
		print '%2d '%partition[i],
	print ''
	for i in range(pn):
		print '%2d '%part[i],
	print ''
	for i in range(pn):
		print '%2d '%sw[i],
	print ''
	edge_cut = 0
	for i in range(sn-1):
		for j in range(i+1, sn):
			if partition[i] != partition[j]:
				edge_cut += l_wei[i][j]	
	print '%d'%edge_cut
