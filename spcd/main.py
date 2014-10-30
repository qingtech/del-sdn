#encoding=utf-8
import copy
import gv
import mlkp_alg
import random_alg
import greedy_alg
import tool
from load_network import load_topo

if __name__=='__main__':

	max_int = 10000
	#输入
	net_topo_file_names = ['33sw.txt','50sw.txt','100sw.txt']
	topo = ['33sw','50sw','100sw']
	nn = ['33','50','100']
	flow_file_names = ['33sw_flow.txt','50sw_flow.txt','100sw_flow.txt']

	
	#输出

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
			pn = 2**level #区域数目
			#mlkp begin
			res = mlkp_alg.switch_partition_and_controller_deployment(level)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			
			
			for pno in part_s_wei.keys():
				output_load.write('mlkp\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno]))

			output_traffic.write('mlkp\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut))
			#mlkp end
			#random begin
			res = random_alg.switch_partition_and_controller_deployment(pn)
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
			part_s_num = res_b[0]
			part_s_wei = res_b[1]
			edge_cut = res_b[2]

			
			
			for pno in part_s_wei.keys():
				output_load.write('random\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno]))

			output_traffic.write('random\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut))
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

			
			
			for pno in part_s_wei.keys():
				output_load.write('greedy\t%s\t%d\t%d\t%d\t%d\n'%(topo[k],pn,pno,part_s_num[pno],part_s_wei[pno]))

			output_traffic.write('greedy\t%s\t%d\t%d\n'%(topo[k],pn,edge_cut))
			#greedy end

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

	
