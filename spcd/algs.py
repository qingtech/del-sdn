#encoding=utf-8
class Result(object):

	def __init__(self, network, algorithm, partition=None, ctr_place=None, part_cost=None, part_s_num=None, part_s_wei=None, inter_traffic=None,):

		assert network
		assert algorithm

		self.network = network
		self.algorithm = algorithm
		self.partition = partition
		self.ctr_place = ctr_place
		self.part_cost = part_cost
		self.part_s_num = part_s_num
		self.part_s_wei = part_s_wei
		self.inter_traffic = inter_traffic

	def get_load_sd():
		print 'hello'
	
class Algorithm(object):

	def __init__(self, name,  network=None, level=None, pn=None):
		assert name
		self.name = name
		#优先遵循level
		if level:
			assert level > 0
			pn = 2**level
		self.network = network
		self.level = level
		self.pn = pn

	def set_network(self, network):
		self.network = network

	def set_level(self, level):
		assert level
		assert level > 0
		self.level = level
		self.pn = 2**level

	def set_pn(self, pn):
		self.pn = pn

	def run(self,):
		'''
		to be override
		'''
