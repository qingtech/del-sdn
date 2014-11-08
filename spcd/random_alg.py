#encoding=utf-8
import sys
import copy
import random
import gv
import initial_partitioning
import tool
from tool import get_s_wei_2,get_child_network,get_res
from network import Network

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

	
if __name__=='__main__':

	max_int = 10000
	#输入
	topo_file_name_list = ['235sw.txt','274sw.txt','349sw.txt']
	topo = ['235sw','274sw','349sw']
	nn = ['235','274','349']
	flow_file_name_list = ['235sw_flow.txt','246sw_flow.txt','300sw_flow.txt']

	
	#输出

	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\tsd\tsd2\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\ttraffic2\tflow\n')


	for k in xrange(3):
		#设置输入：网络拓扑,流矩阵,分区层数
		gv.net_topo_file_name = topo_file_name_list[k]
		gv.flow_file_name = flow_file_name_list[k]

		
		####################
		network = Network(topo_file_name_list[k])
		gv.s_sum = network.sn
		gv.net_topo = network.topo
		gv.s_wei = network.s_wei
		gv.l_wei = network.l_wei
		gv.l_lan = network.path_cost
		s_wei = network.s_wei
		l_wei = network.l_wei
		l_lan = network.path_cost

		sn = gv.s_num
		###################
		print '-----------l_wei----------------------------'
		for i in xrange(sn):
			for j in xrange(sn):
				print '[(%d-> %d),%d]\t'%(i,j,l_wei[i][j]),
			print ''
		print ''
		print '-----------s_wei----------------------------'
		for i in xrange(sn):
			print '[%d,%d]\t'%(i,s_wei[i]),
		print ''



		#算法开始
		for level in xrange(1,6):
			pn = 2**level #区域数目
			sd = {}
			traffic = {}
			sd2 = {}
			traffic2 = {}
			#random begin
			res = switch_partition_and_controller_deployment(pn)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			
			
			sd['random'] = tool.get_standard_deviation(part_s_wei.values())
			traffic['random'] = edge_cut
			sd2['random'] = sd['random']/sd['random']
			traffic2['random'] = float(traffic['random'])/traffic['random']

			for pno in part_s_wei.keys():
				output_load.write('random\t%s\t%d\t%d\t%d\t%d\t%f\t%f\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno],sd['random'],sd2['random']))

			output_traffic.write('random\t%s\t%d\t%d\t%f\t%s\n'%(topo[k],pn,traffic['random'],traffic2['random'],nn[k]))
			print '-------------------------random[%s-%d]-------------------------------\n'%(nn[k],pn)
			print '各个分区的交换机权重总和'
			for pno in part_s_wei.keys():
				print '%2d '%part_s_wei[pno],
			print ''
			print '区域负载标准差：%f'%sd['random']
			print '区域负载标准差2：%f'%sd2['random']
			print '跨域流量（割边）数量：%d'%traffic['random']
			print '跨域流量（割边）数量2：%f'%traffic2['random']
			#random end
