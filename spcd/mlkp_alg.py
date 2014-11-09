#encoding=utf-8
import sys
import copy
import tool
from my_priority_queue import MyPriorityQueue
from network import Network
from algs import Algorithm,Result
from tool import get_s_wei_2,get_child_network,get_res

class MlkpAlg(Algorithm):
	
	def run(self,):

		return self.switch_partition_and_controller_deployment()

	#功能；在所有交换机中选取一个交换机与控制器直接相连，使得控制器与交换机的通讯总体花费最少
	#输入：
	#s_wei[i]表示交换机i需要与交换机进行通讯（包括流建立请求和转发规则下发）的次数
	#path_cost[i][j]表示该链路的“距离”，交换机与控制器的通讯总是走“距离”最短的路径，使用Floyd算法得到
	#输出：
	#i：与控制器直接相连的交换机
	def controller_deployment(self, s_wei, l_wei, path_cost):

		sn = len(s_wei)

		#数据合法性检验
		assert sn > 0
		assert len(path_cost) == sn
		for i in range(sn):
			assert len(path_cost[i]) == sn

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
				tmp_cost += com_num[j]*path_cost[i][j]
			if tmp_cost < cost:
				ii = i
				cost = tmp_cost
		return [ii,cost]

	#功能：划分区域，放置控制器
	#输入：网络拓扑文件名net_topo_file_name,流矩阵文件名flow_file_name,分区层数level（分区数量为：2**level)
	#输出：划分数组part[sn]（sn为交换机数量）,控制器放置数组ctr_place[n_part]
	def switch_partition_and_controller_deployment(self,):
		
		assert self.pn
		assert self.level
		assert self.network
		assert self.network.sn
		assert self.network.s_wei
		assert self.network.path_cost
		#输入
		sn = self.network.sn
		pn = self.pn
		s_wei = network.s_wei
		l_wei = network.l_wei
		path_cost = network.path_cost

		#划分算法开始
		#1.粗化
		#NULL
		#2.初始划分
		partition = self.initial_partition(s_wei, l_wei, path_cost, 0, 1)#迭代二分当前层数0,区域编号从1开始 
		#3.细化
		#NULL
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
			part_no[i+pn] = i+pn
		###################

		ctr_place = {}
		part_cost = {} 
		for pno in part_no.keys():
			ctr_place[pno] = -1
			part_cost[pno] = 0

		for c_part_no in part_no.keys():
			res = get_child_network(s_wei,s_wei_2,l_wei,path_cost,partition,c_part_no)
			if res == None:
				ctr_place[c_part_no] = -1
				part_cost[c_part_no] = 0
				continue
				
			c_s_wei = res[0]
			c_l_wei = res[1]
			c_path_cost = res[2]
			c_index = res[3]
			res = self.controller_deployment(c_s_wei,c_l_wei,c_path_cost)
			ctr_i = res[0]
			ctr_place[c_part_no] = c_index[ctr_i]
			part_cost[c_part_no] = res[1]

		tmp_res = tool.get_res(s_wei, l_wei, path_cost, partition, ctr_place)
		part_s_num = tmp_res[0]
		part_s_wei = tmp_res[1]
		inter_traffic = tmp_res[2]
		res = Result(self.network, self, partition, ctr_place, part_cost, part_s_num, part_s_wei, inter_traffic)

		return res

	#设交换机数量为sn,则
	#s_wei[sn]代表各个交换机的权重
	#l_wei[sn][sn]代表链路权重
	#level代表当传划分的层次,从第0层开始
	#part_no代表当前分区号
	def initial_partition(self, s_wei, l_wei, path_cost, level, part_no):
		#数据合法性检验
		assert self.level > 0
		assert level >= 0 and level <= self.level
			
		sn = len(s_wei)

		assert sn > 0
		assert len(l_wei) == sn
		for i in range(sn):
			assert len(l_wei[i]) == sn

		part = [part_no]*sn
		#最后一层，无需再划分
		if level == self.level:
			return part
		#如果只有一个交换机，无需再划分
		if sn == 1:
			part[0] = part_no*(2**(self.level-level))
			return part
		###############
		'''
		print '----------------l_wei-----------------------'
		for i in xrange(sn):
			print '%2d '%i,
		print ''
		print '--------------------------------------------'
		for i in xrange(sn):
			for j in xrange(sn):
				print '%2d '%l_wei[i][j],
			print ''
		print '----------------s_wei-----------------------'
		for i in xrange(sn):
			print '%2d '%i,
		print ''
		print '--------------------------------------------'
		for i in xrange(sn):
			print '%2d '%s_wei[i],
		print ''
		'''

		###############
		#get bipartition of graph
		#获取两个子分区
		#         1
		#       /   \
		#     /       \
		#    2          3
		#  /  \       /   \
		# 4    5     6     7
		#/ \  / \   / \   / \
		#8 9 10 11 12 13 14 15
		lc_part_no = part_no*2	 	#left  child part
		rc_part_no = part_no*2 + 1	#right child part
		s_wei_2 = [0]*sn
		edge_cut = sys.maxint
		index = -1
		for i in xrange(50):
			tmp_part = tool.randomly_get_bipartition(s_wei, l_wei, lc_part_no, rc_part_no)
			#part = tmp_part
			#break
			#print 'part.len=%d'%len(part)
			#微调左右part
			tmp_part = tool.kernighan_lin_algorithm(s_wei, l_wei, tmp_part, lc_part_no, rc_part_no)
			tmp_edge_cut = 0
			tmp_s_wei_2 = get_s_wei_2(l_wei, tmp_part)
			for j in range(sn):
				tmp_edge_cut += tmp_s_wei_2[j]
			'''
			print 'i=%d, tmp_edge_cut=%d'%(i, tmp_edge_cut)
			print 'tmp_part array'
			for i in range(sn):
				print '%d '%tmp_part[i],
			print ''
			'''
			if tmp_edge_cut < edge_cut:
				edge_cut = tmp_edge_cut
				s_wei_2 = tmp_s_wei_2
				part = tmp_part
				index = i
		#print 'index = %d'%index
		
		'''		
		#left part of bipart
		#right part of bipart
		#统计左右分区交换机个数
		lc_s_num = 0
		rc_s_num = 0
		for i in range(sn):
			if part[i] == lc_part_no:
				lc_s_num +=1
			else:# if part[i] == rc_part_no:
				rc_s_num +=1
		#print 'lc_s_num=%d,rc_s_num=%d'%(lc_s_num,rc_s_num)
		lc_index = [0]*lc_s_num
		rc_index = [0]*rc_s_num
		lc_s_wei = [0]*lc_s_num
		rc_s_wei = [0]*rc_s_num
		lc_l_wei = [[0 for col in xrange(lc_s_num)] for row in xrange(lc_s_num)]
		rc_l_wei = [[0 for col in xrange(rc_s_num)] for row in xrange(rc_s_num)]

		i0 = 0
		i1 = 0
		for i in range(sn):
			if part[i] == lc_part_no:
				lc_index[i0] = i
				lc_s_wei[i0] = s_wei[i] + s_wei_2[i]
				i0 += 1
			else:# if part[i] == rc_part_no:
				rc_index[i1] = i
				rc_s_wei[i1] = s_wei[i] + s_wei_2[i]
				i1 += 1
		#复杂度：O(switch_number^2)
		#lc_l_wei
		for i in xrange(lc_s_num):
			ii = lc_index[i]
			for j in xrange(lc_s_num):
				jj = lc_index[j]
				lc_l_wei[i][j] = l_wei[ii][jj]
		
		#rc_l_wei
		for i in xrange(rc_s_num):
			ii = rc_index[i]
			for j in xrange(rc_s_num):
				jj = rc_index[j]
				rc_l_wei[i][j] = l_wei[ii][jj]
		'''
		#####################
		lc_net = get_child_network(s_wei, s_wei_2, l_wei, path_cost, part, lc_part_no)
		lc_s_wei = lc_net[0]
		lc_l_wei = lc_net[1]
		lc_path_cost = lc_net[2]
		lc_index = lc_net[3]
		rc_net = get_child_network(s_wei, s_wei_2, l_wei, path_cost, part, rc_part_no)
		rc_s_wei = rc_net[0]
		rc_l_wei = rc_net[1]
		rc_path_cost = rc_net[2]
		rc_index = rc_net[3]
		####################
		part_0 = self.initial_partition(lc_s_wei, lc_l_wei, lc_path_cost, level+1, lc_part_no)
		#print 'part.len=%d,part_0.len=%d'%(len(part),len(part_0))
		for i in range(len(lc_s_wei)):
			part[lc_index[i]] = part_0[i]
			#s_wei[lc_index[i]] = lc_s_wei[i]
		part_1 = self.initial_partition(rc_s_wei, rc_l_wei, rc_path_cost, level+1, rc_part_no)
		for i in range(len(rc_s_wei)):
			part[rc_index[i]] = part_1[i]
			#s_wei[rc_index[i]] = rc_s_wei[i]
		return part

if __name__=='__main__':

	#输入
	topo_file_name_list = ['33sw.txt','50sw.txt','100sw.txt']
	topo_name = ['33sw','50sw','100sw']
	topo_count = len(topo_file_name_list)
	flow_file_name_list = ['235sw_flow.txt','246sw_flow.txt','300sw_flow.txt']
	alg_name_dict = {}
	alg_name_dict['mlkp'] = 'mlkp'

	
	#输出

	load_file_name = 'load.txt'
	traffic_file_name = 'traffic.txt'
	output_load = open(load_file_name,'w')
	output_load.write('algs\ttopo\tkway\tpart\tscount\tload\tsd\tsd2\n')
	output_traffic = open(traffic_file_name,'w')
	output_traffic.write('algs\ttopo\tkway\ttraffic\ttraffic2\tflow\n')


	for topo_file_name in topo_file_name_list:
		#设置输入：网络拓扑,流矩阵,分区层数

		####################
		network = Network(topo_file_name)

		###################
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



		#算法开始
		for level in xrange(1,6):
			pn = 2**level #区域数目
			sd = {}
			traffic = {}
			sd2 = {}
			traffic2 = {}
			
			
			#mlkp begin
			alg_name = alg_name_dict['mlkp']
			alg = MlkpAlg(alg_name, network, level, pn)
			res = alg.run()

			part = res.partition
			ctr_place = res.ctr_place
			part_cost = res.part_cost
			part_s_num = res.part_s_num
			part_s_wei = res.part_s_wei
			inter_traffic = res.inter_traffic

			alg_name = res.algorithm.name
			topo_name = res.network.name
			
			sd[alg_name] = tool.get_standard_deviation(part_s_wei.values())
			traffic[alg_name] = inter_traffic
			sd2[alg_name] = sd[alg_name]/sd[alg_name]
			traffic2[alg_name] = float(traffic[alg_name])/traffic[alg_name]

			for pno in part_s_wei.keys():
				output_load.write('%s\t%s\t%d\t%d\t%d\t%d\t%f\t%f\n'%(alg_name, topo_name, pn, pno, part_s_num[pno], part_s_wei[pno],sd[alg_name],sd2[alg_name]))

			output_traffic.write('%s\t%s\t%d\t%d\t%f\t%s\n'%(alg_name, topo_name, pn, traffic[alg_name], traffic2[alg_name], network.sn))
			print '-------------------------%s[%s-%d]-------------------------------\n'%(alg_name, network.sn, pn)
			print '各个分区的交换机权重总和'
			for pno in part_s_wei.keys():
				print '%2d '%part_s_wei[pno],
			print ''
			print '区域负载标准差：%f'%sd[alg_name]
			print '区域负载标准差2：%f'%sd2[alg_name]
			print '跨域流量（割边）数量：%d'%traffic[alg_name]
			print '跨域流量（割边）数量2：%f'%traffic2[alg_name]
			#mlkp end
