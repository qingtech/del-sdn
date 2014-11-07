#encoding=utf-8
import os
import time
import copy
import gv
import mlkp_alg
import random_alg
import greedy_alg
import tool
from load_network import load_topo
from network import Network

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
			res = random_alg.switch_partition_and_controller_deployment(pn)
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
			#greedy begin
			res = greedy_alg.switch_partition_and_controller_deployment(pn)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			
			
			sd['greedy'] = tool.get_standard_deviation(part_s_wei.values())
			traffic['greedy'] = edge_cut
			sd2['greedy'] = sd['greedy']/sd['random']
			traffic2['greedy'] = float(traffic['greedy'])/traffic['random']

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

			#mlkp begin
			res = mlkp_alg.switch_partition_and_controller_deployment(level)
			#res = random_alg.switch_partition_and_controller_deployment(pn)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			sd['mlkp'] = tool.get_standard_deviation(part_s_wei.values())
			traffic['mlkp'] = edge_cut
			sd2['mlkp'] = sd['mlkp']/sd['random']
			traffic2['mlkp'] = float(traffic['mlkp'])/traffic['random']

			for pno in part_s_wei.keys():
				output_load.write('mlkp\t%s\t%d\t%d\t%d\t%d\t%f\t%f\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno],sd['mlkp'],sd2['mlkp']))

			output_traffic.write('mlkp\t%s\t%d\t%d\t%f\t%s\n'%(topo[k],pn,traffic['mlkp'],traffic2['mlkp'],nn[k]))
			print '-------------------------mlkp[%s-%d]-------------------------------\n'%(nn[k],pn)
			print '各个分区的交换机权重总和'
			for pno in part_s_wei.keys():
				print '%2d '%part_s_wei[pno],
			print ''
			print '区域负载标准差：%f'%sd['mlkp']
			print '区域负载标准差2：%f'%sd2['mlkp']
			print '跨域流量（割边）数量：%d'%traffic['mlkp']
			print '跨域流量（割边）数量2：%f'%traffic2['mlkp']
			
			#mlkp end
			

			#是否打印在控制台上
			if False:
			#if True:
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
	
	
