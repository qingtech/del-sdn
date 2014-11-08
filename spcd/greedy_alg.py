#encoding=utf-8
import sys
import copy
import random
import gv
import tool
from network import Network
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



if __name__=='__main__':

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
		###################
		sn = gv.s_num
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
			#greedy begin
			res = switch_partition_and_controller_deployment(pn)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			
			
			sd['greedy'] = tool.get_standard_deviation(part_s_wei.values())
			traffic['greedy'] = edge_cut
			sd2['greedy'] = sd['greedy']/sd['greedy']
			traffic2['greedy'] = float(traffic['greedy'])/traffic['greedy']

			for pno in part_s_wei.keys():
				output_load.write('greedy\t%s\t%d\t%d\t%d\t%d\t%f\t%f\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno],sd['greedy'],sd2['greedy']))

			output_traffic.write('greedy\t%s\t%d\t%d\t%f\t%s\n'%(topo[k],pn,traffic['greedy'],traffic2['greedy'],nn[k]))
			print '-------------------------greedy[%s-%d]-------------------------------\n'%(nn[k],pn)
			print '各个分区的交换机权重总和'
			for pno in part_s_wei.keys():
				print '%2d '%part_s_wei[pno],
			print ''
			print '区域负载标准差：%f'%sd['greedy']
			print '区域负载标准差2：%f'%sd2['greedy']
			print '跨域流量（割边）数量：%d'%traffic['greedy']
			print '跨域流量（割边）数量2：%f'%traffic2['greedy']
			#greedy end


		
