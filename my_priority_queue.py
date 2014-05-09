class MyPriorityQueue(object):
	
	def __init__(self, max_size):
		if max_size <=0:
			print 'invalid parameter, max_size = %d'%max_size
			return
		self.max_size = max_size
		self.queue = [0]*max_size
		self.priority = [0]*max_size
		self.size = 0
	def empty(self):
		return self.size <= 0
	def put(self, pri, ele):
		if self.size >= self.max_size:
			print 'queue is full'
			return
		self.queue[self.size] = ele	
		self.priority[self.size] = pri
		i = self.size
		while i > 0 and self.priority[i-1] < self.priority[i]:
			tmp = self.priority[i-1]
			self.priority[i-1] = self.priority[i]
			self.priority[i] = tmp

			tmp = self.queue[i-1]
			self.queue[i-1] = self.queue[i]
			self.queue[i] = tmp
			
			i -= 1
		self.size += 1
	def update(self, pri, ele):
		index = -1
		for i in xrange(self.size):
			if self.queue[i] == ele:
				index = i
				break
		if index == -1:
			print 'not ele[%d] exist, update failure'%ele
			return
		i = index
		if pri > self.priority[i]:
			self.priority[i] = pri
			while i > 0 and self.priority[i-1] < self.priority[i]:
				tmp = self.priority[i-1]
				self.priority[i-1] = self.priority[i]
				self.priority[i] = tmp

				tmp = self.queue[i-1]
				self.queue[i-1] = self.queue[i]
				self.queue[i] = tmp
			
				i -= 1
	
		else:
			if pri < self.priority[i]:
				self.priority[i] = pri
				while i < (self.size-1) and self.priority[i+1] > self.priority[i]:
					tmp = self.priority[i+1]
					self.priority[i+1] = self.priority[i]
					self.priority[i] = tmp

					tmp = self.queue[i+1]
					self.queue[i+1] = self.queue[i]
					self.queue[i] = tmp
				
					i += 1 
	def get(self):
		if self.size <= 0:
			print 'priority queue is empty, get-operation failure'
			return
		res = self.queue[0]
		del self.queue[0]
		del self.priority[0]
		self.size -= 1
		return res
if __name__ == '__main__':
	pq = MyPriorityQueue(-12)
	pq = MyPriorityQueue(3)
	print 'pq.empty():%d'%pq.empty()
	pq.put(4,8)
	pq.put(3,6)
	pq.put(5,10)
	pq.put(-1,-1)
	print 'pq.size = %d'%pq.size
	print 'pq.empty():%d'%pq.empty()
	#pq.update(12,8)
	for i in xrange(pq.size):
		print '%d '%pq.get(),
	print ''
