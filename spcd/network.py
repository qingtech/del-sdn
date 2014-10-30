#coding:utf-8
import sys
import re
class Network(object):

	def __init__(self, topo, flow = None):
		assert topo
		self.INF = sys.maxint/4 #表示交换机间不可达或者之间不存在链路
		
		#set topo
		#self.topo	#网络拓扑
		#self.sn	#交换机(节点)数目
		#self.l_dist	#链路的距离
		#self.path_succ	#链路后驱矩阵
		#self.path_cost	#路径花费矩阵
		if type(topo) == type('string'):
			topo_file_name = topo
			self.load_topo(topo_file_name)
		else:
			self.set_topo(topo)

		#set flow
		#self.flow	#流矩阵
		#self.s_wei	#流请求数组
		#self.l_wei	#流量矩阵
		sn = len(self.topo)
		if not flow:
			flow = [[1 for col in xrange(sn)] for row in xrange(sn)]
			self.set_flow(flow)
		elif type(flow) == type('string'):
			flow_file_name = flow
			self.load_flow(flow_file_name)
		else:
			self.set_flow(flow)

		
	def load_topo(self, topo_file_name):

		assert topo_file_name

		#load network topology:
		
		f = open(topo_file_name)
		line = f.readline()
		
		assert line

		line = line.strip('\n')

		assert line.isdigit()

		sn = int(line);

		topo = [[0 for col in range(sn)] for row in range(sn)]
		i = 0
		while 1:
			if i >= sn:
				break;
			line = f.readline()
			assert line
			line = line.strip('\n')
			tmp = re.split('\D+',line)
			assert len(tmp) >= sn
			for j in range(sn):
				assert tmp[j].isdigit()
				topo[i][j] = int(tmp[j])
			i += 1
		f.close()
		#set topo
		self.set_topo(topo)

	def set_topo(self, topo):
		assert topo

		sn = len(topo)
		l_dist = [[self.INF for col in range(sn)] for row in range(sn)]
		for i in xrange(sn):
			for j in xrange(sn):
				#topo[i][j] = 0表示交换机i和j之间没有链路, topo[i][j] > 0, 表示i和j之间的距离
				if topo[i][j] > 0:
					l_dist[i][j] = topo[i][j]
		self.sn = len(topo)
		self.topo = topo
		self.l_dist = l_dist
		res = self.floyd(l_dist)
		self.path_succ = res[0]
		self.path_cost = res[1]

	#输入:链路距离矩阵l_dist
	#输出:后驱矩阵path_succ(successor),路径花费矩阵path_cost
	def floyd(self, l_dist):
		sn = len(l_dist)
		path_succ = [[-1 for col in xrange(sn)] for row in xrange(sn)]
		path_cost= [[self.INF for col in xrange(sn)] for row in xrange(sn)]

		for i in xrange(sn):
			for j in xrange(sn):
				path_succ[i][j] = j
				path_cost[i][j] = l_dist[i][j]
		for i in xrange(sn):
			path_succ[i][i] = i
			path_cost[i][i] = 0

		for k in xrange(sn):
			for i in xrange(sn):
				for j in xrange(sn):

					if path_cost[i][j] > (path_cost[i][k] + path_cost[k][j]):
						path_succ[i][j] = path_succ[i][k]
						path_cost[i][j] = path_cost[i][k] + path_cost[k][j]
		return [path_succ,path_cost]

	#输入:网络拓扑矩阵flow
	#输出:交换机权重s_wei(流请求数组),链路权重l_wei(流量矩阵)
	#简述:网络流量矩阵flow存储着任一交换机i到任一交换机j的流的数量,假设flow[i][j]=2,表示交换机i-->j的流
	#     的数量为2,则交换机i需要向控制器发出2个流建立请求,所以s_wei[i]=2,流i-->j根据网络拓扑topo和链路延迟
	#     计算出花费最少的路径(利用Floyd算法求出所有点到点的最短路径),假设为(i-->k-->j),则l_wei[i][k]+=2,l_wei[k][j]+=2
	# run after loading/setting topo
	def load_flow(self, flow_file_name):
		assert flow_file_name
		assert self.topo

		sn = len(topo)

		#load flow:
		
		f = open(flow_file_name)
		
		flow = [[0 for col in xrange(sn)] for row in xrange(sn)]

		while 1:
			line = f.readline()
			if not line:
				break
			line = line.strip('\n') # src_switch dst_switch flow_count
			tmp = re.split('\D+',line)
			assert len(tmp) == 3
			assert tmp[0] < sn	#src_switch, 交换机编号为0,1,2...,sn-1
			assert tmp[1] < sn	#dst_switch, 交换机编号为0,1,2...,sn-1
			assert tmp[2] >= 0	#flow_count, 流的数量必须大于等于0
			flow[tmp[0]][tmp[1]] += tmp[2]
		f.close()
	
		#set flow
		self.set_flow(flow)

	# run after loading/setting topo
	def set_flow(self, flow):
		
		#set flow
		self.flow = flow
		res = self.init_traffic(flow)
		self.s_wei = res[0]
		self.l_wei = res[1]

	def init_traffic(self, flow):
		assert self.topo
		assert self.path_succ
		assert flow
		
		topo = self.topo
		sn = len(topo)
		path_succ = self.path_succ
		assert len(flow) == sn
		
		s_wei = [0]*sn
		l_wei = [[0 for col in xrange(sn)] for row in xrange(sn)]
		for i in xrange(sn):
			for j in xrange(sn):
				s_wei[i] += flow[i][j]
				ii = i
				while True:
					jj = path_succ[ii][j]
					if jj == ii:
						break
					l_wei[ii][jj] += flow[i][j]
					ii = jj
		return [s_wei, l_wei]

	def print_path(self):
		sn = self.sn
		path_cost = self.path_cost
		path_succ = self.path_succ
		for i in xrange(sn):
			for j in xrange(sn):
				print 'path %d to %d, cost = %d'%(i,j,path_cost[i][j])
				ii = i
				print '%d'%(ii),
				while True:
					print '-> %d'%(path_succ[ii][j]),
					ii = path_succ[ii][j]
					if(ii == j):
						print ''
						break;
	def print_wei(self):
		sn = self.sn
		s_wei = self.s_wei
		l_wei = self.l_wei
		print '-----------s_wei----------------------------'
		for i in xrange(sn):
			print '%d:%d\t'%(i,s_wei[i]),
		print ''
		print '-----------l_wei----------------------------'
		for i in xrange(sn):
			for j in xrange(sn):
				print '(%d-> %d):%d\t'%(i,j,l_wei[i][j]),
		print ''

if __name__ == '__main__':
	"""
		    (1)   (3)
		 1——————0——————2
		  \ 	|     /
		   \    |(2) /
		(4) \	|   /(4)
		     \  |  /
		      \ | /
		        3 
	"""
	topo = [[0,1,3,2],[1,0,0,4],[3,0,0,4],[2,4,4,0]]
	
	network = Network(topo)	
	network.print_path()
	network.print_wei()
	
	print 'in topo 33sw'
	topo_file_name = '33sw.txt'
	network = Network(topo_file_name)
	network.print_path()
	network.print_wei()
