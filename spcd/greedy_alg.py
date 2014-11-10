#encoding=utf-8
import sys
import copy
import random
import tool
from network import Network
from algs import Algorithm,Result
from tool import get_s_wei_2,get_child_network,get_res

class GreedyAlg(Algorithm):

	def run(self, network, level=None, pn=None, ):

		super(GreedyAlg, self).run(network, level, pn)

		assert network
		assert pn
		
		self.pn = pn

		return self.switch_partition_and_controller_deployment()

	#功能：划分区域，放置控制器
	#输入：分区数量pn
	#输出：划分数组part[sn]（sn为交换机数量）,控制器放置数组ctr_place[n_part]
	def switch_partition_and_controller_deployment(self,):
		
		assert self.network
		assert self.network.sn
		assert self.pn
		assert self.network.s_wei
		assert self.network.path_cost

		#输入
		sn = self.network.sn
		pn = self.pn
		s_wei = self.network.s_wei
		l_wei = self.network.l_wei
		path_cost = self.network.path_cost


		
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
						tmp_cost += s_wei[j]*path_cost[i][j]
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
					tmp_cost = s_wei[j]*path_cost[ii][j]
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
					
		
		tmp_res = tool.get_res(s_wei, l_wei, path_cost, partition, ctr_place)
		part_sn = tmp_res[0]
		part_s_wei = tmp_res[1]
		inter_traffic = tmp_res[2]
		res = Result(self.network, self, pn, partition, ctr_place, part_cost, part_sn, part_s_wei, inter_traffic)

		return res

if __name__=='__main__':

	#输入
	#拓扑
	topo_file_name_list = ['33sw.txt','50sw.txt','100sw.txt']
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
	alg = GreedyAlg('greedy',)
	alg_dict['greedy'] = alg
	
	#输出

	res_list = []


	for network in net_dict.values():
		for level in xrange(1,6):

			pn = 2**level #区域数目
			for alg in alg_dict.values():

				res = alg.run(network, level, pn)
				res_list.append(res)


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

	base_alg_name = 'greedy'
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
				

	#output
	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\tsd\tsd2\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\ttraffic2\tflow\n')
	for res in res_list:

		part = res.partition
		ctr_place = res.ctr_place
		part_cost = res.part_cost
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
		print '-------------------------%s[%s-%d]-------------------------------\n'%(alg_name, topo_name, pn)
		print '各个分区的交换机权重总和'
		for pno in part_load.keys():
			print '%2d '%part_load[pno],
		print ''
		print '区域负载标准差：%f'%load_sd
		print '区域负载标准差2：%f'%load_sd_2
		print '跨域流量（割边）数量：%d'%inter_traffic
		print '跨域流量（割边）数量2：%f'%inter_traffic_2
