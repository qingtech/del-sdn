#encoding=utf-8
import sys
import copy
import random
import gv
from load_network import load_topo
import initial_partitioning
from tool import get_s_wei_2,get_child_network,get_res


#功能：划分区域，放置控制器
#输入：分区数量pn
#输出：划分数组part[sn]（sn为交换机数量）,控制器放置数组ctr_place[n_part]
def switch_partition_and_controller_deployment(pn):
	
	#输入
	s_wei = gv.s_wei
	l_wei = gv.l_wei
	l_lan = gv.l_lan

	sn = len(s_wei)

	
	partition = [-1]*sn
	ctr_place = {}
	part_cost = {} 

	#求出流请求总量
	sum_s_wei = 0
	for i in xrange(sn):
		sum_s_wei += s_wei[i]

	for k in xrange(pn):
		ctr_place[(k+1)] = -1
		part_cost[(k+1)] = 0
		#贪婪方式选出控制器位置
		cost = sys.maxint
		ii = -1
		for i in range(sn):
			#控制器位置可能和非它管控的交换机直接相连
			if(partition[i] != -1):
				continue
			tmp_cost = 0
			#选出未分配交换机与控制器通讯总花费最小的位置ii
			for j in range(sn):
				if(partition[j] != -1): #未分配交换机
					tmp_cost += s_wei[j]*l_lan[i][j]
			if tmp_cost < cost:
				ii = i
				cost = tmp_cost
		ctr_place[(k+1)] = ii

		#该区域的交换机
		domain_s_wei = 0
		while True:
			jj = -1
			cost = sys.maxint
			for j in xrange(sn):
				if(partition[j] != -1):
					continue
				tmp_cost = s_wei[j]*l_lan[ii][j]
				if tmp_cost < cost:
					jj = j
					cost = tmp_cost
			#表示所有交换机已经分配完成	
			if(jj == -1):
				break;
			#交换机jj分配给区域(k+1)
			partition[jj] = k+1
			part_cost[(k+1)] += cost
			domain_s_wei += s_wei[jj]
			#区域负载是否已经达到
			if(domain_s_wei*pn >= sum_s_wei):
				break;
				
	
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

	#输入
	net_topo_file_names = ['33sw.txt','50sw.txt','100sw.txt']
	topo = ['33sw','50sw','100sw']
	nn = ['33','50','100']
	flow_file_names = ['33sw_flow.txt','50sw_flow.txt','100sw_flow.txt']

	
	#输出
	output_file_name_1 = 'greedy_output.txt'
	output_file_name_2 = 'greedy_output_2.txt'
	out_1 = open(output_file_name_1,'w')
	out_2 = open(output_file_name_2,'w')


	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\n')


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

			res_b = get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

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
				output_load.write('greedy\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno]))
			out_2.write('\n')
			#割边数量，即跨域流量
			out_2.write('跨域流（割边）数量：%d\n'%edge_cut)
			output_traffic.write('greedy\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut))

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

