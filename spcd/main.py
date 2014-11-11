#encoding=utf-8
import os
import time
import copy
import mlkp_alg
import random_alg
import greedy_alg
import tool
from network import Network

if __name__=='__main__':

	#输入
	#拓扑
	topo_file_name_list = ['235sw.txt','274sw.txt','349sw.txt']
	#topo_file_name_list = ['33sw.txt','50sw.txt','100sw.txt']
	#topo_file_name_list = ['33sw.txt',]
	flow_file_name_list = ['235sw_flow.txt','246sw_flow.txt','300sw_flow.txt']
	
	net_dict = {}	
	for topo_file_name in topo_file_name_list:

		network = Network(topo_file_name)
		net_dict[network.name] = network

		s_wei = network.s_wei
		l_wei = network.l_wei
		'''
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
		'''


	#算法
	alg_dict = {}
	alg = random_alg.RandomAlg('random',)
	alg_dict['random'] = alg
	alg = greedy_alg.GreedyAlg('greedy',)
	alg_dict['greedy'] = alg
	alg = mlkp_alg.MlkpAlg('mlkp',)
	alg_dict['mlkp'] = alg

	base_alg_name = 'random'

	#结果

	res_list = []

	for network in net_dict.values():
		for level in xrange(1,6):

			pn = 2**level #区域数目
			for alg in alg_dict.values():

				res = alg.run(network, level, pn)
				res_list.append(res)

				topo_name = res.network.name
				pn = res.pn
				alg_name = res.algorithm.name
				print '-------------------------%s[%s-%d]-------------------------------\n'%(alg_name, topo_name, pn)
				print '各个分区的交换机权重总和'
				for pno in res.part_load.keys():
					print '%2d '%res.part_load[pno],
				print ''
				print '区域负载标准差：%f'%res.load_sd
				#print '区域负载标准差2：%f'%load_sd_2
				print '跨域流量（割边）数量：%d'%res.inter_traffic
				#print '跨域流量（割边）数量2：%f'%inter_traffic_2


	#set load_sd_2, inter_traffic_2
	res_dict = {}
	for res in res_list:
		topo_name = res.network.name
		pn = res.pn
		alg_name = res.algorithm.name
		if not res_dict.get(topo_name, None):
			res_dict[topo_name] = {}
		if not res_dict[topo_name].get(pn, None):
			res_dict[topo_name][pn] = {}
		res_dict[topo_name][pn][alg_name] = res

	for network in net_dict.values():
		topo_name = network.name
		for level in xrange(1,6):
			pn = 2**level #区域数目
			base_res = res_dict[topo_name][pn][base_alg_name]
			for alg in alg_dict.values():
				alg_name = alg.name
				res = res_dict[topo_name][pn][alg_name]
				res.load_sd_2 = float(res.load_sd)/float(base_res.load_sd)
				res.inter_traffic_2 = float(res.inter_traffic)/float(base_res.inter_traffic)


				
				topo_name = res.network.name
				pn = res.pn
				alg_name = res.algorithm.name
				print '-------------------------%s[%s-%d]-------------------------------\n'%(alg_name, topo_name, pn)
				print '各个分区的交换机权重总和'
				for pno in res.part_load.keys():
					print '%2d '%res.part_load[pno],
				print ''
				print '区域负载标准差：%f'%res.load_sd
				print '区域负载标准差2：%f'%res.load_sd_2
				print '跨域流量（割边）数量：%d'%res.inter_traffic
				print '跨域流量（割边）数量2：%f'%res.inter_traffic_2
				

	#输出
	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\tsd\tsd2\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\ttraffic2\tflow\n')
	for res in res_list:

		part = res.partition
		part_sn = res.part_sn
		part_load = res.part_load
		load_sd = res.load_sd
		load_sd_2 = res.load_sd_2
		inter_traffic = res.inter_traffic
		inter_traffic_2 = res.inter_traffic_2

		topo_name = res.network.name
		pn = res.pn
		alg_name = res.algorithm.name
		

		for pno in part_load.keys():
			output_load.write('%s\t%s\t%d\t%d\t%d\t%d\t%f\t%f\n'%(alg_name, topo_name, pn, pno, part_sn[pno], part_load[pno],load_sd,load_sd_2))

		output_traffic.write('%s\t%s\t%d\t%d\t%f\t%s\n'%(alg_name, topo_name, pn, inter_traffic, inter_traffic_2, res.network.sn))
	#输出mlkp算法效果：平均sd_2,最大sd_2,平均inter_traffic_2,最大inter_traffic_2
	mean_load_sd_2 = 0
	max_load_sd_2 = 0
	mean_inter_traffic_2 = 0
	max_inter_traffic_2 = 0
	log_file_name = 'log.txt'
	output_log = open(log_file_name,'w')
	count = 0
	for res in res_list:
		if res.algorithm.name == 'mlkp':
			count += 1
			mean_load_sd_2 += res.load_sd_2
			mean_inter_traffic_2 += res.inter_traffic_2
			if max_load_sd_2 < res.load_sd_2:
				max_load_sd_2 = res.load_sd_2
			if max_inter_traffic_2 < res.inter_traffic_2:
				max_inter_traffic_2 = res.inter_traffic_2
	mean_load_sd_2 = float(mean_load_sd_2)/count	
	mean_inter_traffic_2 = float(mean_inter_traffic_2)/count
	
	output_log.write('%f\t%f\t%f\t%f\n'%(mean_load_sd_2, max_load_sd_2, mean_inter_traffic_2, max_inter_traffic_2))
