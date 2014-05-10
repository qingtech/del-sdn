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
debug = True
#功能：根据链路权重l_wei将中间路径建立请求添加到s_wei
#输入：
#s_wei：初始路径建立请求
#l_wei: 链路权重
#输出：
#s_wei2: 中间路径建立请求
def get_s_wei_2(s_wei, l_wei, part):
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
	for i in range(sn-1):
		for j in range(i+1,sn):
			if part[i] != part[j]:
				s_wei_2[i] += l_wei[j][i]
				s_wei_2[j] += l_wei[i][j]
	return s_wei_2
#功能：求出权重数组s_wei[]的总和。
#输入：s_wei[]
#输出：sum_s_wei
def get_sum_s_wei(s_wei):
	sum = 0
	for sw in s_wei:
		sum += sw
	return sum
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
	s_wei_2 = []
	#左右分区交换机权重不超过总权重0.1%
	#如果经过count仍找不到符合以上条件的左右分区，则取count中最佳
	while abs(rsw-lsw) > (rsw + lsw)*0.1:
		rsw = lsw = 0
		tmp_part = [0]*sn
		#将初始路径请求（域内流）添加到lsw和rsw
		for i in range(sn):
			if random.randint(0,1) == 0:
				tmp_part[i] = lc_part_no
				lsw += s_wei[i]
			else:
				tmp_part[i] = rc_part_no
				rsw += s_wei[i]
		#将中间路径请求（跨域流）添加到lsw和rsw
		tmp_s_wei_2 = get_s_wei_2(s_wei, l_wei, tmp_part)
		for i in range(sn):
			if tmp_part[i] == lc_part_no:
				rsw += tmp_s_wei_2[i]
			else:
				lsw += tmp_s_wei_2[i]
		#比较该次划分和比历史最好划分
		if d > abs(rsw-lsw):
			part = tmp_part
			d = abs(rsw-lsw)
			s_wei_2 = tmp_s_wei_2
		count -= 1
		if count <= 0:
			break
	#print 's_wei_2[0] = %d'%tmp_s_wei_2[0]
	if debug:
		edge_cut = get_sum_s_wei(s_wei_2)
		lsn = rsn = 0
		lsw = rsw = 0
		for i in xrange(sn):
			if part[i] == lc_part_no:
				lsn += 1
				lsw += (s_wei[i] + s_wei_2[i])
			else:
				rsn += 1
				rsw += (s_wei[i] + s_wei_2[i])
		print '----------------------------------------------------------------------'
		print 'randomly_get_bipartiton'
		print 'edge_cut = %d'%edge_cut
		print 'lsn = %d, rsn = %d'%(lsn,rsn)
		print 'abs(lsw-rsw)*1.0/(lsw+rsw) = ',
		print 'abs(%d-%d)*1.0/(%d+%d) = %f'%(lsw,rsw,lsw,rsw,(abs(lsw-rsw)*1.0/(lsw+rsw)))
	return part
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
	check = [False]*sn
	#初始化gain[]
	for i in xrange(sn):
		for j in xrange(sn):
			if part[i] == part[j]:
				gain[i] -= l_wei[i][j] + l_wei[j][i]
			else:
				gain[i] += l_wei[i][j] + l_wei[j][i]
	pq0 = MyPriorityQueue(sn)
	pq1 = MyPriorityQueue(sn)
	#初始化两个优先队列
	for i in xrange(sn):
		if part[i] == lc_part_no:
			pq0.put(gain[i],i)
		else:
			pq1.put(gain[i],i)
	lc_sum_sw = 0
	rc_sum_sw = 0
	s_wei_2 = get_s_wei_2(s_wei, l_wei, part)
	#初始路径&中间路径建立请求
	###########
	lc_sw_1 = rc_sw_1 = 0
	lc_sw_2 = rc_sw_2 = 0
	###########
	for i in xrange(sn):
		if part[i] == lc_part_no:
				   #初始路径   中间路径
			lc_sum_sw += s_wei[i] + s_wei_2[i]
			#########
			lc_sw_1 += s_wei[i]
			lc_sw_2 += s_wei_2[i]
			#########
		else:
			rc_sum_sw += s_wei[i] + s_wei_2[i]
			#########
			rc_sw_1 += s_wei[i]
			rc_sw_2 += s_wei_2[i]
			#########
	edge_cut = 0
	#计算当前edge_cut
	for i in range(sn):
		edge_cut += s_wei_2[i]
	#根据两个优先队列，遍历每个节点
	tmp_edge_cut = edge_cut
	for i in xrange(sn):
		index = -1
		if debug:
			print 'lc_sum_sw = %3d, rc_sum_sw = %3d'%(lc_sum_sw, rc_sum_sw)
			#print 'lc_sw_1 = %3d, rc_sw_1 = %3d'%(lc_sw_1, rc_sw_1)
			#print 'lc_sw_2 = %3d, rc_sw_2 = %3d'%(lc_sw_2, rc_sw_2)
		if lc_sum_sw > rc_sum_sw:
			if pq0.empty():
				break	
			index = pq0.get()
		else:	
			if pq1.empty():
				break
			index = pq1.get()
		if debug:
			if part[index] == lc_part_no:
				print 'part[%2d] = %d = lc_part_no'%(index,part[index])
			else:
				print 'part[%2d] = %d = rc_part_no'%(index,part[index])
		ec[i] = tmp_edge_cut - gain[index]
		tmp_edge_cut = ec[i]
		shift[i] = index
		if part[index] == lc_part_no:
			lc_sum_sw -= s_wei[index]
			rc_sum_sw += s_wei[index]
			################
			lc_sw_1 -= s_wei[index]
			rc_sw_1 += s_wei[index]
			################
		else:
			lc_sum_sw += s_wei[index]
			rc_sum_sw -= s_wei[index]
			################
			lc_sw_1 += s_wei[index]
			rc_sw_1 -= s_wei[index]
			################
		#重新调整与交换机index相邻的交换机的gain
		for j in xrange(sn):
			if j == index:
				continue
			if part[index] == lc_part_no:
				if part[j] == lc_part_no:
					s_wei_2[index] += l_wei[j][index]
					s_wei_2[j] += l_wei[index][j]
					rc_sum_sw += l_wei[j][index]
					lc_sum_sw += l_wei[index][j]
					########################
					rc_sw_2 += l_wei[j][index]
					lc_sw_2 += l_wei[index][j]
					########################
					#必须乘以2,囧。。。2BUG
					gain[j] += (l_wei[index][j] + l_wei[j][index])*2
					if not check[j]:
						pq0.update(gain[j], j)
				else:
					s_wei_2[index] -= l_wei[j][index]
					s_wei_2[j] -= l_wei[index][j]
					rc_sum_sw -= l_wei[j][index]
					lc_sum_sw -= l_wei[index][j]
					########################
					rc_sw_2 -= l_wei[j][index]
					lc_sw_2 -= l_wei[index][j]
					########################
					gain[j] -= (l_wei[index][j] + l_wei[j][index])*2
					if not check[j]:
						pq1.update(gain[j], j)
			else:
				if part[j] == lc_part_no:
					s_wei_2[index] -= l_wei[j][index]
					s_wei_2[j] -= l_wei[index][j]
					rc_sum_sw -= l_wei[j][index]
					lc_sum_sw -= l_wei[index][j]
					########################
					lc_sw_2 -= l_wei[j][index]
					rc_sw_2 -= l_wei[index][j]
					########################
					gain[j] -= (l_wei[index][j] + l_wei[j][index])*2
					if not check[j]:
						pq0.update(gain[j], j)
				else:
					s_wei_2[index] += l_wei[j][index]
					s_wei_2[j] += l_wei[index][j]
					lc_sum_sw += l_wei[j][index]
					rc_sum_sw += l_wei[index][j]
					########################
					lc_sw_2 += l_wei[j][index]
					rc_sw_2 += l_wei[index][j]
					########################
					gain[j] += (l_wei[index][j] + l_wei[j][index])*2
					if not check[j]:
						pq1.update(gain[j], j)
		#标记交换机 index
		check[index] = True
		if part[index] == lc_part_no:
			part[index] = rc_part_no
		else:
			part[index] = lc_part_no
	#选取取得最小edge-cut的放置
	index = -1
	tmp_edge_cut = edge_cut 
	for i in xrange(sn):
		if ec[i] < tmp_edge_cut:
			index = i
			tmp_edge_cut = ec[i]
	#将取得最小edge-cut后续的shift undone
	edge_cut = tmp_edge_cut
	for i in xrange(index+1, sn):
		if shift[i] == -1:
			'''
			if debug:
				print 'shift[%d] = -1'%i
			'''
			break
		j = shift[i]
		if part[j] == lc_part_no:
			part[j] = rc_part_no
		else:
			part[j] = lc_part_no
	if debug:
		s_wei_2 = get_s_wei_2(s_wei, l_wei, part)
		lc_sum_sw = rc_sum_sw = 0
		tmp_edge_cut = 0
		lsn = rsn = 0
		for i in xrange(sn):
			if part[i] == lc_part_no:
				lc_sum_sw += (s_wei[i] + s_wei_2[i])
				lsn += 1
			else:
				rc_sum_sw += (s_wei[i] + s_wei_2[i])
				rsn += 1
			tmp_edge_cut += s_wei_2[i]
		print 'kernighan_lin_algorithm'
		print 'edge_cut = %d'%edge_cut
		print 'lsn = %d, rsn = %d'%(lsn,rsn)
		print 'abs(lsw-rsw)*1.0/(lsw+rsw) = ',
		print 'abs(%d-%d)*1.0/(%d+%d) = %f'%(lc_sum_sw,rc_sum_sw,lc_sum_sw,rc_sum_sw,(abs(lc_sum_sw-rc_sum_sw)*1.0/(lc_sum_sw+rc_sum_sw)))
		print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	return part

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
	part = [part_no]*sn
	'''
	###############
	print '----------------l_wei-----------------------'
	for i in xrange(sn):
		print '%2d '%i,
	print ''
	print '--------------------------------------------'
	for i in xrange(sn):
		for j in xrange(sn):
			print '%2d '%l_wei[i][j],
		print ''
	###############
	'''
	#最后一层，无需再划分
	if level == gv.level:
		return part
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
	s_wei_2 = [0]*sn
	edge_cut = sys.maxint
	index = -1
	for i in range(5):
		tmp_part = randomly_get_bipartition(s_wei, l_wei, lc_part_no, rc_part_no)
		#part = tmp_part
		#break
		#print 'part.len=%d'%len(part)
		#微调左右part
		tmp_part = kernighan_lin_algorithm(s_wei, l_wei, tmp_part, lc_part_no, rc_part_no)
		tmp_edge_cut = 0
		tmp_s_wei_2 = get_s_wei_2(s_wei, l_wei, tmp_part)
		for j in range(sn):
			tmp_edge_cut += tmp_s_wei_2[j]
		'''
		print 'i=%d, tmp_edge_cut=%d'%(i, tmp_edge_cut)
		print 'tmp_part array'
		for i in range(sn):
			print '%d '%tmp_part[i],
		print ''
		'''
		if tmp_edge_cut < edge_cut:
			edge_cut = tmp_edge_cut
			s_wei_2 = tmp_s_wei_2
			part = tmp_part
			index = i
	#print 'index = %d'%index
		
	#left part of bipart
	#right part of bipart
	#统计左右分区交换机个数
	lc_s_num = 0
	rc_s_num = 0
	for i in range(sn):
		if part[i] == lc_part_no:
			lc_s_num +=1
		else:# if part[i] == rc_part_no:
			rc_s_num +=1
	#print 'lc_s_num=%d,rc_s_num=%d'%(lc_s_num,rc_s_num)
	lc_index = [0]*lc_s_num
	rc_index = [0]*rc_s_num
	lc_s_wei = [0]*lc_s_num
	rc_s_wei = [0]*rc_s_num
	lc_l_wei = [[0 for col in range(lc_s_num)] for row in range(lc_s_num)]
	rc_l_wei = [[0 for col in range(rc_s_num)] for row in range(rc_s_num)]
	'''
	what a f*cking bug 囧。。。。。
	#rc_l_wei = [[0]*rc_s_num]*rc_s_num
	'''
	#index,s_wei
	i0 = 0
	i1 = 0
	for i in range(sn):
		if part[i] == lc_part_no:
			lc_index[i0] = i
			lc_s_wei[i0] = s_wei[i] + s_wei_2[i]
			i0 += 1
		else:# if part[i] == rc_part_no:
			rc_index[i1] = i
			rc_s_wei[i1] = s_wei[i] + s_wei_2[i]
			i1 += 1
	#复杂度：O(switch_number^2)
	#lc_l_wei
	for i in xrange(lc_s_num):
		ii = lc_index[i]
		for j in xrange(lc_s_num):
			jj = lc_index[j]
			lc_l_wei[i][j] = l_wei[ii][jj]
	'''
	#################
	flag = False
	print 'lc_l_wei'
	for i in range(lc_s_num):
		print '%2d '%lc_index[i],
	print ''
	print '----------------------------------------------------------'
	for i in range(lc_s_num):
		for j in xrange(lc_s_num):
			print '%2d '%(lc_l_wei[i][j]),
			flag = lc_l_wei[i][j] - lc_l_wei[j][i]
		print ''
	#################
	'''
	#rc_l_wei
	for i in xrange(rc_s_num):
		ii = rc_index[i]
		for j in xrange(rc_s_num):
			jj = rc_index[j]
			rc_l_wei[i][j] = l_wei[ii][jj]
	'''
	########################
	flag = False	
	print 'rc_l_wei'
	for i in range(rc_s_num):
		print '%2d '%rc_index[i],
	print ''
	print '----------------------------------------------------------'
	for i in range(rc_s_num):
		for j in xrange(rc_s_num):
			print '%2d '%(rc_l_wei[i][j]),
			flag = rc_l_wei[i][j] - rc_l_wei[j][i]
		print ''
	########################
	'''
	part_0 = initial_partition(lc_s_wei,lc_l_wei,level+1, lc_part_no)
	#print 'part.len=%d,part_0.len=%d'%(len(part),len(part_0))
	for i in range(lc_s_num):
		part[lc_index[i]] = part_0[i]
		s_wei[lc_index[i]] = lc_s_wei[i]
	part_1 = initial_partition(rc_s_wei,rc_l_wei,level+1, rc_part_no)
	for i in range(rc_s_num):
		part[rc_index[i]] = part_1[i]
		s_wei[rc_index[i]] = rc_s_wei[i]
	return part
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
	partition = initial_partition(s_wei, l_wei, 0, 1)
	pn = 2**gv.level
	part_s_num = [0]*pn
	part_s_wei   = [0]*pn
	s_wei_2 = get_s_wei_2(s_wei, l_wei, partition)
	print 'switch weight'
	for i in range(sn):
		print '%2d '%s_wei[i],
	print ''
	print '交换机分区情况'
	for i in range(sn):
		part_s_num[partition[i]-pn] += 1
		part_s_wei[partition[i]-pn] += s_wei[i] + s_wei_2[i]
		print '%2d '%partition[i],
	print ''
	print '各个分区交换机数量'
	for i in range(pn):
		print '%2d '%part_s_num[i],
	print ''
	print '各个分区的交换机权重总和'
	for i in range(pn):
		print '%2d '%part_s_wei[i],
	print ''
	edge_cut = 0
	for i in range(sn):
		edge_cut += s_wei_2[i]
	print '割边数量：%d'%edge_cut
