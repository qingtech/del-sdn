#encoding:utf-8
import gv
import load_topo
import sys
import error
import random
import copy
from my_priority_queue import MyPriorityQueue
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'
#功能：根据链路权重l_wei将中间路径建立请求添加到s_wei
#输入：
#s_wei：初始路径建立请求
#l_wei: 链路权重
#输出：
#s_wei2: 中间路径建立请求
def get_s_wei_2(s_wei, l_wei, part, lc_part_no, rc_part_no):
	sn = len(s_wei)
	#数据合法性检验
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_wei) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_wei[i]) != sn:
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(part) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	#算法开始
	s_wei_2 = [0]*sn
	for i in range(sn):
		for j in range(sn):
			if part[i] == lc_part_no and part[j] == rc_part_no:
				s_wei_2[i] += l_wei[j][i]
				s_wei_2[j] += l_wei[i][j]
	return s_wei_2
#功能：将父分区根据交换机权重划分为总权重大致相等的两个子分区
#输入：
#父分区交换机权重数组：s_wei[]
#左子分区号：lc_part_no
#右子分区号：rc_part_no
#输出：
#分区数组：partition[]
#复杂度：O(switch_number^2)
def randomly_get_bipartition(s_wei, l_wei, lc_part_no, rc_part_no):
	sum_s_wei = 0	#顶点总权重
	count = 100	#寻找分区最大循环次数
	for sw in s_wei:
		sum_s_wei += sw
	sn = len(s_wei)
	part = [0]*sn
	lsw = 0
	rsw = sum_s_wei
	d = abs(rsw-lsw)
	#左右分区交换机权重不超过总权重0.1%
	#如果经过count仍找不到符合以上条件的左右分区，则取count中最佳
	while abs(rsw-lsw) > (rsw + lsw)0.1:
		rsw = lsw = 0
		tmp = [0]*sn
		#将初始路径请求（域内流）添加到lsw和rsw
		for i in range(sn):
			if random.randint(0,1) == 0:
				tmp[i] = lc_part_no
				lsw += s_wei[i]
			else:
				tmp[i] = rc_part_no
				rsw += s_wei[i]
		#将中间路径请求（跨域流）添加到lsw和rsw
		s_wei_2 = get_s_wei_2(s_wei, l_wei, part, lc_part_no, rc_part_no)
		for i in range(sn):
			if tmp[i] == lc_part_no:
				rsw += s_wei_2[i]
			else:
				lsw += s_wei_2[i]
		#比较该次划分和比历史最好划分
		if d > abs(rsw-lsw):
			part = tmp
			d = abs(rsw-lsw)
		count -= 1
		if count <= 0:
			break
	return partition
#功能：根据随机划分好的两个分区，通过Kernighan-Lin算法对其进行调整，使得edge-cut达到最少
#输入：交换机权重s_wei[]，链路权重l_wei[][]，划分数组part[]
def kernighan_lin_algorithm(s_wei, l_wei, part, lc_part_no, rc_part_no):
	sn = len(s_wei)
	#数据合法性检验
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_wei) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_wei[i]) != sn:
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(part) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	#算法开始	
	max = 1000000000 
	gain = [0]*sn
	ec = [max]*sn
	shift = [-1]*sn
	#初始化gain[]
	for i in xrange(sn):
		for j in xrange(sn):
			if part[i] == part[j]:
				gain[i] -= l_wei[i][j] + l_wei[j][i]
			else:
				gain[i] += l_wei[i][j] + l_wei[j][i]
	pq0 = MyPriorityQueue()
	pq1 = MyPriorityQueue()
	#初始化两个优先队列
	for i in xrange(sn):
		if part[i] == lc_part_no:
			pq0.put(gain[i],i)
		else:
			pq1.put(gain[i],i)
	edge_cut = 0
	#计算当前edge_cut
	for i in xrange(sn - 1):
		for j in xrange(i, sn):
			if part[i] != part[j]:
				edge_cut += l_wei[i][j] + l_wei[j][i]
	lc_sum_sw = 0
	rc_sum_sw = 0
	s_wei_2 = get_s_wei_2(s_wei, l_wei, part, lc_part_no, rc_part_no)
	#初始路径&中间路径建立请求
	for i in xrange(sn):
		if part[i] == lc_part_no:
				   #初始路径   中间路径
			lc_sum_sw += s_wei[i] + s_wei_2[i]
		else:
			rc_sum_sw += s_wei[i] + s_wei_2[i]
	#根据两个优先队列，遍历每个节点
	for i in xrange(sn):
		index = -1
		if lc_sum_sw > rc_sum_sw:
			if pq0.empty():
				break	
			index = pq0.get()
		else:	
			if pq1.empty():
				break
			index = pq0.get()
		ec[i] = edge_cut - gain[index]
		edge_cut = ec[i]
		shift[i] = index
		s_wei_2[index] = 0
		#重新调整与交换机index相邻的交换机的gain
		for j in xrange(sn):
			if part[index] == lc_part_no:
				lc_sum_sw -= s_wei[index]
				rc_sum_sw += s_wei[index]
				if part[j] = lc_part_no:
					lc_sum_sw += l_wei[index][j]
					gain[j] += (l_wei[index][j] + l_wei[j][index])
					pq0.update(gain[j], j)
				else:
					gain[j] -= (l_wei[index][j] + l_wei[j][index])
					pq1.update(gain[j], j)
			else:
				lc_sum_sw += s_wei[index]
				rc_sum_sw -= s_wei[index]
				if part[j] = lc_part_no:
					gain[j] -= (l_wei[index][j] + l_wei[j][index])
					pq0.update(gain[j], j)
				else:
					gain[j] += (l_wei[index][j] + l_wei[j][index])
					pq1.update(gain[j], j)
		#调整交换机 index
		gain[index] = -gain[index]
		if part[index] == lc_part_no:
			part[index] = rc_part_no
		else:
			part[index] = lc_part_no
	#选取取得最小edge-cut的放置
	index = 0
	edge_cut = ec[0]
	for i in xrange(sn):
		if ec[i] < edge_cut:
			index = i
			edge_cut = ec[i]
	#将取得最小edge-cut后续的shift undone
	for i in xrange(index+1, sn):
		if shift[i] == -1:
			break
		j = shift[i]
		if part[j] == lc_part_no:
			part[j] = rc_part_no
		else:
			part[j] = lc_part_no
#设交换机数量为sn,则
#s_wei[sn]代表各个交换机的权重
#l_wei[sn][sn]代表链路权重
#level代表当传划分的层次,从第0层开始
#part_no代表当前分区号
def initial_partition(s_wei,l_wei,level,part_no):
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
		
	partition = [part_no]*sn
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
	lc_part_no = part_no*2	 	#left  child part
	rc_part_no = part_no*2 + 1	#right child part
	edge_cut = sys.maxint
	tmp_s_wei = []
	for i in range(5):
		tmp_s_wei = copy.deepcopy(s_wei)
		tmp_part = randomly_get_bipartition(tmp_s_wei, l_wei, lc_part_no, rc_part_no)
		partition = tmp_part
		break
		#print 'partition.len=%d'%len(partition)
		#微调左右partition
		kernighan_lin_algorithm(tmp_s_wei, l_wei, tmp_part, lc_part_no, rc_part_no)
		tmp = 0
		for j in range(sn):
			for k in range(sn):
				if tmp_part[j] != tmp_part[k]:
					tmp += l_wei[j][k]
		if tmp < edge_cut:
			edge_cut = tmp
			partition = tmp_part
		
	#update s_wei
	for i in range(sn):
		s_wei[i] = tmp_s_wei[i]
	#part 0 of bipartition
	#part 1 of bipartition
	#统计左右分区交换机个数
	sn0 = 0
	sn1 = 0
	for i in range(sn):
		if partition[i] == lc_part_no:
			sn0 +=1
		else:# if partition[i] == rc_part_no:
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
		if partition[i] == lc_part_no:
			index_0[i0] = i
			s_wei_0[i0] = s_wei[i]
			i0 += 1
		else:# if partition[i] == rc_part_no:
			index_1[i1] = i
			s_wei_1[i1] = s_wei[i]
			i1 += 1
	#复杂度：O(switch_number^2)
	#l_wei_0
	ii = 0
	#print 'sn0=%d,sn1=%d'%(sn0,sn1)
	for i in range(sn):
		if partition[i] == lc_part_no:
			#print 'ii=%d'%ii
			jj = 0
			for j in range(sn):
				if partition[j] == lc_part_no:
					l_wei_0[ii][jj] = l_wei[i][j]
					#print '%d '%jj
					jj += 1
			ii += 1	

	#l_wei_1
	ii = 0
	for i in range(sn):
		if partition[i] == rc_part_no:
			jj = 0	
			for j in range(sn):
				if partition[j] == rc_part_no:
					l_wei_1[ii][jj] = l_wei[i][j]
					jj += 1
			ii += 1	
	part_0 = initial_partition(s_wei_0,l_wei_0,level+1, lc_part_no)
	#print 'partition.len=%d,part_0.len=%d'%(len(partition),len(part_0))
	for i in range(sn0):
		#print 'i=%d,index_0[i]=%d'%(i,index_0[i])
		partition[index_0[i]] = part_0[i]
		s_wei[index_0[i]] = s_wei_0[i]
	part_1 = initial_partition(s_wei_1,l_wei_1,level+1, rc_part_no)
	for i in range(sn1):
		partition[index_1[i]] = part_1[i]
		s_wei[index_1[i]] = s_wei_1[i]
	return partition
if __name__ == '__main__':
	#sn = 16*1
	#s_wei =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	#l_wei = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] for row in range(sn)]
	max = 1000000000
	load_topo.load_topo()
	sn = gv.s_num
	s_wei = [1]*sn
	l_wei = copy.deepcopy(gv.net_topo)
	l_lan = copy.deepcopy(gv.net_topo)
	for i in range(sn):
		for j in range(sn):
			if l_wei[i][j] == 0:
				l_lan[i][j] = max
	'''
	print 'l_wei'
	for i in range(sn):
		for j in range(sn):
			print '%d '%l_wei[i][j],
		print ''
	print 'l_lan'
	for i in range(sn):
		for j in range(sn):
			print '%d '%l_lan[i][j],
		print ''
	print 'gv.net_topo'
	for i in range(sn):
		for j in range(sn):
			print '%d '%gv.net_topo[i][j],
		print ''
	'''
	partition = initial_partition( s_wei, l_wei, 0, 1)
	pn = 2**gv.level
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
	for i in range(sn):
		for j in range(sn):
			if partition[i] != partition[j]:
				edge_cut += l_wei[i][j]	
	print '割边数量：%d'%edge_cut
