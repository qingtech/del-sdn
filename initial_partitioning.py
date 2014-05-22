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
debug = False 
#功能：得到左右分区权重差因子
#输入：左分区交换机总权重lc_sum_sw，右分区交换机总权重rc_sum_sw
#输出：
#左右分区权重差因子
def get_partition_factor(lc_sum_sw, rc_sum_sw):
	return abs(lc_sum_sw - rc_sum_sw)*1.0/(lc_sum_sw + rc_sum_sw)
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
#功能：求出分区part_no的权重总和
def get_sum_s_wei_by_part(s_wei, part, part_no):
	sum = 0
	for i in xrange(len(s_wei)):
		if part[i] == part_no:
			sum += s_wei[i]
	return sum
#功能求出交换机index从src_part_no转移到dst_part_no后的gain
#输入：index,src_part_no,dst_part_no,part,s_wei,l_wei,sum_sw[src_sw_1,src_sw_2,dst_sw_1,dst_sw_2],src_pq,dst_pq,gain,check
#输出：sum_sw[src_sw_1,src_sw_2,dst_sw_1,dst_sw_2]
def get_gain(index,src_part_no,dst_part_no,part,s_wei,l_wei,sum_sw,src_pq = None,dst_pq = None,gain = None,gain_2 = None,check = None):
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

	src_sw_1 = sum_sw[0]
	src_sw_2 = sum_sw[1]
	dst_sw_1 = sum_sw[2]
	dst_sw_2 = sum_sw[3]

	src_sw_1 -= s_wei[index]
	dst_sw_1 += s_wei[index]

	#重新调整与交换机index相邻的交换机的gain
	for j in xrange(sn):
		if j == index:
			continue
		if part[j] == src_part_no:
			########################
			dst_sw_2 += l_wei[j][index]
			src_sw_2 += l_wei[index][j]
			########################
			if gain != None:
				#必须乘以2,囧。。。2BUG
				gain[j] += (l_wei[index][j] + l_wei[j][index])*2
		if part[j] == dst_part_no:
			########################
			src_sw_2 -= l_wei[j][index]
			dst_sw_2 -= l_wei[index][j]
			########################
			if gain != None:
				gain[j] -= (l_wei[index][j] + l_wei[j][index])*2
	if gain != None:
		for j in xrange(sn):
			if j == index:
				continue
			if not check[j]:
				part[index] = dst_part_no
				if part[j] == src_part_no:
					tmp_sum_sw = [src_sw_1,src_sw_2,dst_sw_1,dst_sw_2]
					tmp_res = get_gain(j,src_part_no,dst_part_no,part,s_wei,l_wei,tmp_sum_sw)
					gain_2[j] = tmp_res[6]
					src_pq.update(gain[j],gain_2[j],j)
				if part[j] == dst_part_no:
					tmp_sum_sw = [dst_sw_1,dst_sw_2,src_sw_1,src_sw_2]
					tmp_res = get_gain(j,dst_part_no,src_part_no,part,s_wei,l_wei,tmp_sum_sw)
					gain_2[j] = tmp_res[6]
					dst_pq.update(gain[j],gain_2[j],j)
				part[index] = src_part_no
				
	src_sum_sw = src_sw_1 + src_sw_2
	dst_sum_sw = dst_sw_1 + dst_sw_2
	#print 'src_sum_sw = %d, dst_sum_sw = %d'%(src_sum_sw,dst_sum_sw)
	if len(part) == 1:
		print 'src_sum_sw = %d, dst_sum_sw = %d'%(src_sum_sw,dst_sum_sw)
		print 'sum_sw[0] = %d'%sum_sw[0]
		print 'sum_sw[1] = %d'%sum_sw[1]
		print 'sum_sw[2] = %d'%sum_sw[2]
		print 'sum_sw[3] = %d'%sum_sw[3]
		print 'gain = %s'%gain
		print 'part[0] = %d'%part[0]
		print 'src_part_no = %d'%src_part_no
		print 'dst_part_no = %d'%dst_part_no
	#print 'len(part) = %d'%len(part)
	part_factor = get_partition_factor(src_sum_sw, dst_sum_sw)
	#print 'part_factor = %f'%part_factor
	res = [src_sw_1,src_sw_2,dst_sw_1,dst_sw_2,src_sum_sw,dst_sum_sw,part_factor]
	return res
	################################################################
#功能：获得分区号为c_part_no的分区子网络
#输入：s_swei[],s_wei_2[],l_wei[][],part,c_part_no
#输出：分区子网络_net_topo[c_s_wei[],c_l_wei[]],对应父网络的交换机编号c_index[]
def get_child_network(s_wei,s_wei_2,l_wei,part,c_part_no):
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

	#统计分区交换机个数
	c_s_num = 0
	for i in range(sn):
		if part[i] == c_part_no:
			c_s_num +=1

	c_index = [0]*c_s_num
	c_s_wei = [0]*c_s_num
	c_l_wei = [[0 for col in xrange(c_s_num)] for row in xrange(c_s_num)]
	'''
	what a f*cking bug 囧。。。。。
	c_l_wei = [[0]*c_s_num]*c_s_num
	'''
	#index,s_wei
	ii = 0
	for i in xrange(sn):
		if part[i] == c_part_no:
			c_index[ii] = i
			c_s_wei[ii] = s_wei[i] + s_wei_2[i]
			ii += 1
	#复杂度：O(switch_number^2)
	#c_l_wei
	for i in xrange(c_s_num):
		ii = c_index[i]
		for j in xrange(c_s_num):
			jj = c_index[j]
			c_l_wei[i][j] = l_wei[ii][jj]
	res = [c_s_wei,c_l_wei,c_index]
	return res

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
	part = [rc_part_no]*sn
	lsw = 0
	rsw = sum_s_wei
	f = 1.0
	s_wei_2 = []
	#左右分区交换机权重不超过总权重0.1%
	#如果经过count仍找不到符合以上条件的左右分区，则取count中最佳
	while f > 0.1:
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
		tmp_f = get_partition_factor(lsw,rsw)
		#print 'lsw = %d, rsw = %d'%(lsw,rsw)
		#print 'tmp_f = %f'%tmp_f
		if f > tmp_f:
			part = tmp_part
			f = tmp_f
			s_wei_2 = tmp_s_wei_2
		count -= 1
		if count <= 0:
			break
	#print 's_wei_2[0] = %d'%tmp_s_wei_2[0]
	if debug:
	#if True:
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
		#print '----------------------------------------------------------------------'
		#print 'randomly_get_bipartiton'
		#print 'edge_cut = %d'%edge_cut
		#print 'lsn = %d, rsn = %d'%(lsn,rsn)
		#print 'lsw = %d, rsw = %d'%(lsw,rsw)
		#print 'fffff = %f'%(get_partition_factor(lsw,rsw))
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
	max = sys.maxint/2 
	gain = [0]*sn
	gain_2 = [0.0]*sn
	ec = [max]*sn
	th = [0.0]*sn
	shift = [-1]*sn
	check = [False]*sn
	#初始化gain[]
	#计算交换机权重
	#初始路径&中间路径建立请求
	s_wei_2 = get_s_wei_2(s_wei, l_wei, part)
	lc_sw_1 = get_sum_s_wei_by_part(s_wei, part, lc_part_no)
	rc_sw_1 = get_sum_s_wei_by_part(s_wei, part, rc_part_no)
	lc_sw_2 = get_sum_s_wei_by_part(s_wei_2, part, lc_part_no)
	rc_sw_2 = get_sum_s_wei_by_part(s_wei_2, part, rc_part_no)
	lc_sum_sw = lc_sw_1 + lc_sw_2
	rc_sum_sw = rc_sw_1 + rc_sw_2 
	edge_cut = lc_sw_2 + rc_sw_2
	for i in xrange(sn):
		for j in xrange(sn):
			if part[i] == part[j]:
				gain[i] -= l_wei[i][j] + l_wei[j][i]
			else:
				gain[i] += l_wei[i][j] + l_wei[j][i]
		tmp_res = []
		if part[i] == lc_part_no:
			sum_sw = [lc_sw_1,lc_sw_2,rc_sw_1,rc_sw_2]
			tmp_res = get_gain(i,lc_part_no,rc_part_no,part,s_wei,l_wei,sum_sw)
		else:
			sum_sw = [rc_sw_1,rc_sw_2,lc_sw_1,lc_sw_2]
			tmp_res = get_gain(i,rc_part_no,lc_part_no,part,s_wei,l_wei,sum_sw)
		gain_2[i] = tmp_res[6] 
	pq0 = MyPriorityQueue(sn)
	pq1 = MyPriorityQueue(sn)
	#初始化两个优先队列
	for i in xrange(sn):
		if part[i] == lc_part_no:
			pq0.put(gain[i],gain_2[i],i)
		else:
			pq1.put(gain[i],gain_2[i],i)
		
	#根据两个优先队列，遍历每个节点
	tmp_edge_cut = edge_cut
	for i in xrange(sn):
		index = -1
		if debug:
			print 'lc_sum_sw = %3d, rc_sum_sw = %3d'%(lc_sum_sw, rc_sum_sw)
			print 'lc_sw_1 = %3d, rc_sw_1 = %3d'%(lc_sw_1, rc_sw_1)
			print 'lc_sw_2 = %3d, rc_sw_2 = %3d'%(lc_sw_2, rc_sw_2)
			if lc_sw_2 < 0 or rc_sw_2 < 0:
				print 'error!!!!!!!'
				content = raw_input('error')
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
		#检查转移交换机index是否会使两个分区的交换机权重更加不平衡
		#################cc
		#暂时将交换机index转移到另一个分区
		if part[index] == lc_part_no:
			part[index] = rc_part_no
		else:
			part[index] = lc_part_no

		tmp_s_wei_2 = get_s_wei_2(s_wei, l_wei, part)
		tmp_lc_sum_sw = get_sum_s_wei_by_part(s_wei, part, lc_part_no) + get_sum_s_wei_by_part(tmp_s_wei_2, part, lc_part_no)
		tmp_rc_sum_sw = get_sum_s_wei_by_part(s_wei, part, rc_part_no) + get_sum_s_wei_by_part(tmp_s_wei_2, part, rc_part_no)
		#将交换机index转回到原分区
		if part[index] == lc_part_no:
			part[index] = rc_part_no
		else:
			part[index] = lc_part_no
		if debug:
			if get_partition_factor(tmp_lc_sum_sw, tmp_rc_sum_sw) > 0.2 :
				print 'tmp_lc_sum_sw = %d, tmp_rc_sum_sw = %d'%(tmp_lc_sum_sw, tmp_rc_sum_sw)
				print 'lc_sum_sw = %d, rc_sum_sw = %d'%(lc_sum_sw, rc_sum_sw)
				content = raw_input('got bad partition factor if shift')
		#################cc
		####################dd
		tmp_res = []
		if part[index] == lc_part_no:
			sum_sw = [lc_sw_1,lc_sw_2,rc_sw_1,rc_sw_2]
			tmp_res = get_gain(index,lc_part_no,rc_part_no,part,s_wei,l_wei,sum_sw,pq0,pq1,gain,gain_2,check)
			lc_sw_1 = tmp_res[0]
			lc_sw_2 = tmp_res[1]
			rc_sw_1 = tmp_res[2]
			rc_sw_2 = tmp_res[3]
			lc_sum_sw = tmp_res[4]
			rc_sum_sw = tmp_res[5]
		else:
			sum_sw = [rc_sw_1,rc_sw_2,lc_sw_1,lc_sw_2]
			tmp_res = get_gain(index,rc_part_no,lc_part_no,part,s_wei,l_wei,sum_sw,pq1,pq0,gain,gain_2,check)
			lc_sw_1 = tmp_res[2]
			lc_sw_2 = tmp_res[3]
			rc_sw_1 = tmp_res[0]
			rc_sw_2 = tmp_res[1]
			lc_sum_sw = tmp_res[5]
			rc_sum_sw = tmp_res[4]
		#lc_sum_sw = lc_sw_1 + lc_sw_2
		#rc_sum_sw = rc_sw_1 + rc_sw_2
		####################dd
		#标记交换机 index
		ec[i] = tmp_edge_cut - gain[index]
		th[i] = tmp_res[6]
		tmp_edge_cut = ec[i]
		shift[i] = index
		check[index] = True
		if part[index] == lc_part_no:
			part[index] = rc_part_no
		else:
			part[index] = lc_part_no
	#选取取得最小edge-cut的放置
	index = -1
	tmp_edge_cut = edge_cut 
	#print '*******************************'
	for i in xrange(sn):
		#print 'i=%d,th[i]=%f'%(i,th[i])
		#print 'ec[i] = %d'%ec[i]
		if th[i]<0.1 and ec[i] < tmp_edge_cut:
			index = i
			tmp_edge_cut = ec[i]
	#将取得最小edge-cut后续的shift undone
	edge_cut = tmp_edge_cut
	#print 'index=%d,th[index]=%f'%(index,th[index])
	#print 'edge_cut = %d'%edge_cut
	for i in xrange(index+1, sn):
		if shift[i] == -1:
			'''
			if debug:
				print 'shift[%d] = -1'%i
			'''
			continue	
		j = shift[i]
		if part[j] == lc_part_no:
			part[j] = rc_part_no
		else:
			part[j] = lc_part_no
	if debug:
	#if True:
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
	#最后一层，无需再划分
	if level == gv.level:
		return part
	#如果只有一个交换机，无需再划分
	if sn == 1:
		part[0] = part_no*(2**(gv.level-level))
		return part
	###############
	'''
	print '----------------l_wei-----------------------'
	for i in xrange(sn):
		print '%2d '%i,
	print ''
	print '--------------------------------------------'
	for i in xrange(sn):
		for j in xrange(sn):
			print '%2d '%l_wei[i][j],
		print ''
	print '----------------s_wei-----------------------'
	for i in xrange(sn):
		print '%2d '%i,
	print ''
	print '--------------------------------------------'
	for i in xrange(sn):
		print '%2d '%s_wei[i],
	print ''
	'''

	###############
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
	for i in xrange(50):
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
	
	'''		
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
	lc_l_wei = [[0 for col in xrange(lc_s_num)] for row in xrange(lc_s_num)]
	rc_l_wei = [[0 for col in xrange(rc_s_num)] for row in xrange(rc_s_num)]

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
	
	#rc_l_wei
	for i in xrange(rc_s_num):
		ii = rc_index[i]
		for j in xrange(rc_s_num):
			jj = rc_index[j]
			rc_l_wei[i][j] = l_wei[ii][jj]
	'''
	#####################
	lc_net = get_child_network(s_wei,s_wei_2,l_wei,part,lc_part_no)
	lc_s_wei = lc_net[0]
	lc_l_wei = lc_net[1]
	lc_index = lc_net[2]
	rc_net = get_child_network(s_wei,s_wei_2,l_wei,part,rc_part_no)
	rc_s_wei = rc_net[0]
	rc_l_wei = rc_net[1]
	rc_index = rc_net[2]
	####################
	part_0 = initial_partition(lc_s_wei,lc_l_wei,level+1, lc_part_no)
	#print 'part.len=%d,part_0.len=%d'%(len(part),len(part_0))
	for i in range(len(lc_s_wei)):
		part[lc_index[i]] = part_0[i]
		#s_wei[lc_index[i]] = lc_s_wei[i]
	part_1 = initial_partition(rc_s_wei,rc_l_wei,level+1, rc_part_no)
	for i in range(len(rc_s_wei)):
		part[rc_index[i]] = part_1[i]
		#s_wei[rc_index[i]] = rc_s_wei[i]
	return part
if __name__ == '__main__':
	#sn = 16*1
	#s_wei =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	#l_wei = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] for row in range(sn)]
	max = sys.maxint
	gv.net_topo_file_name = 'os3e.txt'
	load_topo.load_topo()
	sn = gv.s_num
	s_wei = [1]*sn
	l_wei = copy.deepcopy(gv.net_topo)
	l_lan = copy.deepcopy(gv.net_topo)
	for i in range(sn):
		for j in range(sn):
			if l_wei[i][j] == 0:
				l_lan[i][j] = max
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

