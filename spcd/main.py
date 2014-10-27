#encoding=utf-8
import copy
import gv
import mlkp
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
			#res = switch_partition_and_controller_deployment(net_topo_file_names[k],flow_file_names[k],level)
			res = mlkp.switch_partition_and_controller_deployment(level)
			pn = 2**level
			part = res[0]
			ctr_place = res[1]
			part_cost = res[2]

			##############reomve after function get_res() with no bugs#################
			res_b = tool.get_res(s_wei, l_wei, l_lan, part,ctr_place)
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

	
