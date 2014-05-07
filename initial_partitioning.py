#encoding:utf-8
import gv
import load_topo
import sys
import error
import random
import copy
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'

#功能：将父分区根据交换机权重划分为总权重大致相等的两个子分区
#输入：
#父分区交换机权重数组：s_wei[]
#左子分区号：lc_part_no
#右子分区号：rc_part_no
#输出：
#分区数组：partition[]
#复杂度：O(switch_number^2)
def randomly_get_bipartition(s_wei, l_wei, lc_part_no, rc_part_no):
	sum_wei = 0	#顶点总权重
	sum_wei2 = 0	#因划分而产生的额外顶点权重（跨域流的中间路径建立请求）
	count = 100	#寻找分区最大循环次数
	for sw in s_wei:
		sum_wei += sw
	sn = len(s_wei)
	partition = [0]*sn
	lsw = 0
	rsw = sum_wei
	d = abs(rsw-lsw)
	#左右分区交换机权重不超过总权重0.1%
	#如果经过count仍找不到符合以上条件的左右分区，则取count中最佳
	while abs(rsw-lsw) > (sum_wei + sum_wei2)*0.1:
		rsw = lsw = 0
		sum_wei2 = 0
		tmp = [0]*sn
		for i in range(sn):
			if random.randint(0,1) == 0:
				tmp[i] = lc_part_no
				lsw += s_wei[i]
			else:
				tmp[i] = rc_part_no
				rsw += s_wei[i]
		#将因分区而新增的中间路径请求（跨域流）添加到lsw和rsw
		for i in range(sn):
			for j in range(sn):
				if tmp[i] == lc_part_no and tmp[j] == rc_part_no:
					#i(left)————j(right)
					#i————>j
					rsw += l_wei[i][j]
					#i<————j
					lsw += l_wei[j][i]
					sum_wei2 += l_wei[i][j] + l_wei[j][i]
				'''
				else if tmp[i] == rc_part_no and tmp[j] == lc_part_no:
					rsw += l_wei[i][j]
					lsw += l_wei[j][i]
					sum_wei2 += l_wei[i][j] + l_wei[j][i]
				'''	
		if d > abs(rsw-lsw):
			partition = tmp
			d = abs(rsw-lsw)
		count -= 1
		if count <= 0:
			break
	for i in range(sn):
		for j in range(sn):
			if partition[i] == lc_part_no and partition[j] == rc_part_no:
				s_wei[i] += l_wei[j][i]
				s_wei[j] += l_wei[i][j]
			'''
			else if partition[i] == rc_part_no and partition[j] == lc_part_no:
				s_wei[i] += l_wei[i][j]
				s_wei[j] += l_wei[j][i]
			'''
	return partition

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
		tmp = 0
		for j in range(sn-1):
			for k in range(j,sn):
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
