#encoding=utf-8
class Result(object):

	def __init__(self, network, algorithm, pn, partition, ctr_place, part_cost, part_sn, part_load, inter_traffic,):

		assert network
		assert algorithm
		assert pn
		assert partition
		assert ctr_place
		assert part_cost
		assert part_sn
		assert part_load
		assert inter_traffic

		self.network = network
		self.algorithm = algorithm
		self.pn = pn
		self.partition = partition
		self.ctr_place = ctr_place
		self.part_cost = part_cost
		self.part_sn = part_sn
		self.part_load = part_load
		self.inter_traffic = inter_traffic

		import tool
		self.load_sd = tool.get_standard_deviation(self.part_load.values())
		
		#TO be set
		self.load_sd_2 = None
		self.inter_traffic_2 = None


		
	
class Algorithm(object):

	def __init__(self, name,):
		assert name
		self.name = name

		#to be set in function run()
		self.network = None
		self.level = None
		self.pn = None

	def set_network(self, network):
		self.network = network

	def set_level(self, level):
		assert level
		assert level > 0
		self.level = level
		self.pn = 2**level

	def set_pn(self, pn):
		self.pn = pn

	def run(self, network, level=None, pn=None, ):
		assert network

		self.network = network

		'''
		to be overide
		'''
