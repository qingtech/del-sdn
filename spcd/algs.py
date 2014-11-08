class Result(object):

	def __init__(self,):

class Algorithm(object):
	
	def __init__(self, network=None, level=None, pn=None):
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
