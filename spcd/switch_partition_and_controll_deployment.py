#encoding=utf-8
import gv
import error
import load_topo
import sys
import copy
import initial_partitioning
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'

#功能：根据链路权重l_wei将中间路径建立请求添加到s_wei
#输入：
#s_wei：初始路径建立请求(似乎不需要该参数）
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

#功能：获得分区号为c_part_no的分区子网络
#输入：s_swei[],s_wei_2[],l_wei[][],part,c_part_no
#输出：分区子网络_net_topo[c_s_wei[],c_l_wei[]],对应父网络的交换机编号c_index[]
def get_child_network(s_wei,s_wei_2,l_wei,l_lan,part,c_part_no):
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
	#如果不存在该分区子网络
	if c_s_num == 0:
		return None
	c_index = [0]*c_s_num
	c_s_wei = [0]*c_s_num
	c_l_wei = [[0 for col in xrange(c_s_num)] for row in xrange(c_s_num)]
	c_l_lan = [[0 for col in xrange(c_s_num)] for row in xrange(c_s_num)]
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
			c_l_lan[i][j] = l_lan[ii][jj]
	res = [c_s_wei,c_l_wei,c_l_lan,c_index]
	return res
#功能；在所有交换机中选取一个交换机与控制器直接相连，使得控制器与交换机的通讯总体花费最少
#输入：
#s_wei[i]表示交换机i需要与交换机进行通讯（包括流建立请求和转发规则下发）的次数
#l_lan[i][j]表示该链路的“距离”，交换机与控制器的通讯总是走“距离”最短的路径，使用Floyd算法得到
#输出：
#i：与控制器直接相连的交换机
def controller_deployment(s_wei,l_wei,l_lan):
	#数据合法性检验
	sn = len(s_wei)
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_lan) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_lan[i]) != sn:
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
	#算法开始
	#每个交换机和控制器通讯的次数（流建立请求，规则下发）
	com_num = [0]*sn
	for i in xrange(sn):
		#流建立请求（包括回应）
		com_num[i] = s_wei[i]*2
		for j in xrange(sn):
			#规则建立部分
				com_num[i] += l_wei[j][i]
	cost = sys.maxint
	ii = -1
	for i in range(sn):
		tmp_cost = 0
		for j in range(sn):
			tmp_cost += s_wei[j]*l_lan[i][j]
		if tmp_cost < cost:
			ii = i
			cost = tmp_cost
	if False:
	#if True:
		#最短路径矩阵
		print '最短路径矩阵：'
		for i in range(sn):
			for j in range(sn):
				if l_lan[i][j] == sys.maxint/4:
					print 'x ',
				else:
					print '%d '%l_lan[i][j],
			print ''
		print '通讯总花费：%d'%cost 
		print '+++++++++++++++++++++++++++++++++++++++++'
	#print '通讯总花费：%d'%cost 
	#print '+++++++++++++++++++++++++++++++++++++++++'
	return [ii,cost]
#功能：划分区域，放置控制器
#输入：网络拓扑文件名net_topo_file_name，分区层数level（分区数量为：2**level)
#输出：划分数组part[sn]（sn为交换机数量）,控制器放置数组ctr_place[n_part]
def switch_partition_and_controller_deployment(net_topo_file_name,level):
	max = sys.maxint/4
	gv.net_topo_file_name = net_topo_file_name
	load_topo.load_topo()
	gv.level = level
	sn = gv.s_num
	s_wei = [1]*sn
	l_wei = copy.deepcopy(gv.net_topo)
	l_lan = copy.deepcopy(gv.net_topo)
	for i in range(sn):
		for j in range(sn):
			if l_wei[i][j] == 0:
				l_lan[i][j] = max
	#Floyd最短路径
	for i in range(sn):
		for j in range(sn):
			for k in range(sn):
				if l_lan[i][k] + l_lan[k][j] < l_lan[i][j]:
					l_lan[i][j] = l_lan[i][k] + l_lan[k][j]
					        #层数，分区号
	partition = initial_partitioning.initial_partition(s_wei, l_wei, 0, 1)
	pn = 2**gv.level
	part_s_num = [0]*pn
	part_s_wei   = [0]*pn
	s_wei_2 = get_s_wei_2(s_wei, l_wei, partition)
	edge_cut = 0
	edge_not_cut = 0	#edge_not_cut = sum(l_wei) - edge_cut
	for i in range(sn):
		edge_cut += s_wei_2[i]
	for i in xrange(sn):
		for j in xrange(sn):
			edge_not_cut += l_wei[i][j]
	edge_not_cut -= edge_cut

	ctr_place = [-1]*pn
	part_cost = [0]*pn
	for c_part_no in xrange(pn,pn*2):
		res = get_child_network(s_wei,s_wei_2,l_wei,l_lan,partition,c_part_no)
		if res == None:
			ctr_place[c_part_no-pn] = -1
			part_cost[c_part_no-pn] = 0
			continue
			
		c_s_wei = res[0]
		c_l_wei = res[1]
		c_l_lan = res[2]
		c_index = res[3]
		res = controller_deployment(c_s_wei,c_l_wei,c_l_lan)
		ctr_i = res[0]
		ctr_place[c_part_no-pn] = c_index[ctr_i]
		part_cost[c_part_no-pn] = res[1]
	for i in range(sn):
		part_s_num[partition[i]-pn] += 1
		part_s_wei[partition[i]-pn] += s_wei[i] + s_wei_2[i]
	if False:
	#if True:
		print '控制器放置位置：'
		for i in xrange(pn):
			print '%2d '%(i+pn),
		print ''
		for i in xrange(pn):
			print '%2d '%ctr_place[i],
		print ''
		print '********************************************************'
		print '交换机编号'
		for i in xrange(sn):
			print '%2d '%i,
		print ''
		print '交换机权重：'
		for i in range(sn):
			print '%2d '%(s_wei[i]+s_wei_2[i]),
		print ''
		print '交换机分区情况'
		for i in range(sn):
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
		print '割边数量：%d'%edge_cut
	
		#分区结果，控制器位置，区域交换机数量，区域负载(交换机总权重)，跨域流（割边），区域花费
	return [partition,ctr_place,part_s_num,part_s_wei,edge_cut,edge_not_cut,part_cost]
if __name__ == '__main__':
	#输入：网络拓扑矩阵file，网络流量矩阵file，划分区域数，(链路延迟）
	#输出：区域负载，域内流数量，跨域流（割边）数量,分区结果，(控制器放置)
	max = 10000
	"""
		    (1)(2)(1)
		(2)1————0————2(10)
		     	|
			|(1)
		     	|
		     	3(2)
	"""
	s_wei = [2,2,10,2]
	l_lan = [[0,1,1,1],[1,0,max,max],[1,max,0,max],[1,max,max,0]]
	l_wei = [[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0]]
	i = controller_deployment(s_wei,l_wei,l_lan)[0]
	if False:
		print 'i=%d'%i
		print 'switch partition and controller placement:'
	fn = ['33sw.txt','50sw.txt','100sw.txt']
	nn = ['33','50','100']
	output_file_name_1 = 'output.txt'
	output_file_name_2 = 'output_2.txt'
	out_1 = open(output_file_name_1,'w')
	out_2 = open(output_file_name_2,'w')
	for k in xrange(3):
		for level in xrange(1,6):
			res = switch_partition_and_controller_deployment(fn[k],level)
			pn = 2**level
			part = res[0]
			ctr_place = res[1]
			part_s_num = res[2]
			part_s_wei = res[3]
			edge_cut = res[4]
			edge_not_cut = res[5]
			part_cost = res[6]
			#交换机数量为nn[k],分区数量为pn
			#[nn[k],pn],例如：[33,2]
			out_1.write('[%s-%d]\n'%(nn[k],pn))
			out_2.write('[%s-%d]\n'%(nn[k],pn))
			for i in xrange(pn,2*pn):
				#列出分区编号为i的所有交换机，后一个为控制器所在的交换机位置
				#例如：1,2,3,1 该分区有交换机1,2,3并且控制器与交换机1直接相连
				for j in xrange(len(part)):
					if part[j] == i:
						out_1.write('%d,'%j)
						out_2.write('%d,'%j)
				out_1.write('%d\n'%ctr_place[i-pn])
				out_2.write('%d\n'%ctr_place[i-pn])
			
			
			out_2.write('各个分区交换机数量\n')
			for i in xrange(len(part_s_num)):
				out_2.write('%2d '%part_s_num[i])
			out_2.write('\n')
			out_2.write('各个分区的交换机权重总和\n')
			for i in xrange(len(part_s_wei)):
				out_2.write('%2d '%part_s_wei[i])
			out_2.write('\n')
			#割边数量，即跨域流数量
			out_2.write('跨域流（割边）数量：%d\n'%edge_cut)
			#域内流数量
			out_2.write('域内流数量：%d\n'%edge_not_cut)

			out_2.write('交换机分区情况\n')
			for i in xrange(len(part)):
				out_2.write('%2d '%part[i])
			out_2.write('\n')
			
			out_2.write('控制器放置位置\n')
			for i in xrange(len(ctr_place)):
				out_2.write('%2d '%(2**level+i))
			out_2.write('\n')
			for i in xrange(len(ctr_place)):
				out_2.write('%2d '%ctr_place[i])
			out_2.write('\n')
			out_2.write('各个分区花费代价\n')
			for i in xrange(len(part_cost)):
				out_2.write('%2d '%part_cost[i])
			out_2.write('\n')
			out_2.write('--------------------------------------------------------\n')
			#是否打印在控制台上
			#if False:
			if True:
				print '-------------------------[%s-%d]-------------------------------\n'%(nn[k],pn)
				print '各个分区交换机数量'
				for i in xrange(len(part_s_num)):
					print '%2d '%part_s_num[i],
				print ''
				print '各个分区的交换机权重总和'
				for i in xrange(len(part_s_wei)):
					print '%2d '%part_s_wei[i],
				print ''
				print '跨域流（割边）数量：%d'%edge_cut
				print '域内流数量：%d'%edge_not_cut

				print '交换机分区情况'
				for i in xrange(len(part)):
					print '%2d '%part[i],
				print ''
				print '控制器放置位置'
				for i in xrange(len(ctr_place)):
					print '%2d '%(2**level+i),
				print ''
				for i in xrange(len(ctr_place)):
					print '%2d '%ctr_place[i],
				print ''
				print '各个分区花费代价'
				for i in xrange(len(part_cost)):
					print '%2d '%part_cost[i],
				print ''

