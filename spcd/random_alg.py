#encoding=utf-8
import sys
import copy
import random
import gv
from load_network import load_topo
import initial_partitioning
from tool import get_s_wei_2,get_child_network,get_res

def random_partition(sn, pn):
	partition = [0]*sn

	for i in xrange(sn):
		partition[i] = random.randint(1,pn)

	return partition

#功能；在所有交换机中选取一个交换机与控制器直接相连，使得控制器与交换机的通讯总体花费最少
#输入：
#s_wei[i]表示交换机i需要与交换机进行通讯（包括流建立请求和转发规则下发）的次数
#l_lan[i][j]表示该链路的“距离”，交换机与控制器的通讯总是走“距离”最短的路径，使用Floyd算法得到
#输出：
#i：与控制器直接相连的交换机
def controller_deployment(s_wei,l_wei,l_lan):
	#数据合法性检验
	sn = len(s_wei)
	assert sn > 0
	assert len(l_lan) == sn
	for i in range(sn):
		assert len(l_lan[i]) == sn

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
#输入：分区数量pn
#输出：划分数组part[sn]（sn为交换机数量）,控制器放置数组ctr_place[n_part]
def switch_partition_and_controller_deployment(pn):
	
	#输入
	s_wei = gv.s_wei
	l_wei = gv.l_wei
	l_lan = gv.l_lan

	sn = len(s_wei)

	#划分算法开始
	#随机获得划分结果
 	partition = random_partition(sn, pn)
	#划分算法结束
	
	#放置算法开始
	s_wei_2 = get_s_wei_2(l_wei, partition)
	#获取part_no
	part_no = {}
	#无法保证分区数量为pn
	#for i in range(sn):
	#	part_no[partition[i]] = partition[i]
	####################
	#修改如下
	for i in xrange(pn):
		part_no[i+1] = i+1
	###################

	ctr_place = {}
	part_cost = {} 
	for pno in part_no.keys():
		ctr_place[pno] = -1
		part_cost[pno] = 0

	for c_part_no in part_no.keys():
		res = get_child_network(s_wei,s_wei_2,l_wei,l_lan,partition,c_part_no)
		if res == None:
			ctr_place[c_part_no] = -1
			part_cost[c_part_no] = 0
			continue
			
		c_s_wei = res[0]
		c_l_wei = res[1]
		c_l_lan = res[2]
		c_index = res[3]
		res = controller_deployment(c_s_wei,c_l_wei,c_l_lan)
		ctr_i = res[0]
		ctr_place[c_part_no] = c_index[ctr_i]
		part_cost[c_part_no] = res[1]

	return [partition, ctr_place, part_cost]

if __name__ == '__main__':
	#输入：网络拓扑矩阵file，流矩阵file，划分区域数，(链路延迟）
	#输出：区域负载，域内流数量，跨域流（割边）数量,分区结果，(控制器放置)
	max_int = 10000
	"""
		    (1)(2)(1)
		(2)1————0————2(10)
		     	|
			|(1)
		     	|
		     	3(2)
	"""
	s_wei = [2,2,10,2]
	l_lan = [[0,1,1,1],[1,0,max_int,max_int],[1,max_int,0,max_int],[1,max_int,max_int,0]]
	l_wei = [[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0]]
	i = controller_deployment(s_wei,l_wei,l_lan)[0]
	if False:
		print 'i=%d'%i
		print 'switch partition and controller placement:'
	#输入
	net_topo_file_names = ['33sw.txt','50sw.txt','100sw.txt']
	topo = ['33sw','50sw','100sw']
	nn = ['33','50','100']
	flow_file_names = ['33sw_flow.txt','50sw_flow.txt','100sw_flow.txt']

	
	#输出
	output_file_name_1 = 'output.txt'
	output_file_name_2 = 'output_2.txt'
	out_1 = open(output_file_name_1,'w')
	out_2 = open(output_file_name_2,'w')


	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\n')

	##############reomve after function get_res() with no bugs#################
	load_file_name_b = 'load_b.txt'
	traffic_file_name_b = 'traffic_b.txt'
	output_load_b = open(load_file_name_b,'w')
	output_load_b.write('algs\ttopo\tkway\tpart\tscount\tload\n')
	output_traffic_b = open(traffic_file_name_b,'w')
	output_traffic_b.write('algs\ttopo\tkway\ttraffic\n')
	##############reomve after function get_res() with no bugs#################

	for k in xrange(3):
		#设置输入：网络拓扑,流矩阵,分区层数
		gv.net_topo_file_name = net_topo_file_names[k]
		gv.flow_file_name = flow_file_names[k]
		load_topo()

		sn = gv.s_num
		s_wei = [1]*sn
		l_wei = copy.deepcopy(gv.net_topo)
		l_lan = copy.deepcopy(gv.net_topo)
		for i in range(sn):
			for j in range(sn):
				if l_wei[i][j] == 0:
					l_lan[i][j] = max_int
		#Floyd最短路径
		for i in xrange(sn):
			for j in xrange(sn):
				for r in xrange(sn):
					if l_lan[i][r] + l_lan[r][j] < l_lan[i][j]:
						l_lan[i][j] = l_lan[i][r] + l_lan[r][j]
		gv.s_wei = s_wei
		gv.l_wei = l_wei
		gv.l_lan = l_lan

		#算法开始
		for level in xrange(1,6):
			pn = 2**level
			res = switch_partition_and_controller_deployment(pn)
			pn = 2**level
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			##############reomve after function get_res() with no bugs#################
			res_b = get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num_b = res_b[0]
			part_s_wei_b = res_b[1]
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]
			edge_cut_b = res_b[2]

			for pno in part_s_wei_b.keys():
				output_load_b.write('mlkp\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num_b[pno],part_s_wei_b[pno]))
			output_traffic_b.write('mlkp\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut_b))
			##############reomve after function get_res() with no bugs#################
			#交换机数量为nn[k],分区数量为pn
			#[nn[k],pn],例如：[33,2]
			out_1.write('[%s-%d]\n'%(nn[k],pn))
			out_2.write('[%s-%d]\n'%(nn[k],pn))
			for pno in ctr_place.keys():
				#列出分区编号为pno的所有交换机，后一个为控制器所在的交换机位置
				#例如：1,2,3,1 该分区有交换机1,2,3并且控制器与交换机1直接相连
				for j in xrange(len(part)):
					if part[j] == pno:
						out_1.write('%d,'%j)
						out_2.write('%d,'%j)
				out_1.write('%d\n'%ctr_place[pno])
				out_2.write('%d\n'%ctr_place[pno])
			
			
			out_2.write('各个分区交换机数量\n')
			for pno in part_s_num.keys():
				out_2.write('%2d '%part_s_num[pno])
			out_2.write('\n')
			out_2.write('各个分区的交换机权重总和\n')
			for pno in part_s_wei.keys():
				out_2.write('%2d '%part_s_wei[pno])
				output_load.write('mlkp\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno]))
			out_2.write('\n')
			#割边数量，即跨域流数量
			out_2.write('跨域流（割边）数量：%d\n'%edge_cut)
			output_traffic.write('mlkp\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut))

			out_2.write('交换机分区情况\n')
			for i in xrange(len(part)):
				out_2.write('%2d '%part[i])
			out_2.write('\n')
			
			out_2.write('控制器放置位置\n')
			for pno in ctr_place.keys():
				out_2.write('%2d '%(pno))
			out_2.write('\n')
			for pno in ctr_place.keys():
				out_2.write('%2d '%ctr_place[pno])
			out_2.write('\n')
			out_2.write('各个分区花费代价\n')
			for pno in part_cost.keys():
				out_2.write('%2d '%part_cost[pno])
			out_2.write('\n')
			out_2.write('--------------------------------------------------------\n')
			#是否打印在控制台上
			#if False:
			if True:
				print '-------------------------[%s-%d]-------------------------------\n'%(nn[k],pn)
				print '各个分区交换机数量'
				for pno in part_s_num.keys():
					print '%2d '%part_s_num[pno],
				print ''
				print '各个分区的交换机权重总和'
				for pno in part_s_wei.keys():
					print '%2d '%part_s_wei[pno],
				print ''
				print '跨域流量（割边）数量：%d'%edge_cut

				print '交换机分区情况'
				for i in xrange(len(part)):
					print '%2d '%part[i],
				print ''
				print '控制器放置位置'
				for pno in ctr_place.keys():
					print '%2d '%(pno),
				print ''
				for pno in ctr_place.keys():
					print '%2d '%ctr_place[pno],
				print ''
				print '各个分区花费代价'
				for pno in part_cost.keys():
					print '%2d '%part_cost[pno],
				print ''

