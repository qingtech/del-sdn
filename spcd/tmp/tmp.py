import time
print 'self'
nlist = [0,1]
nlist = [float(i)/1000000 for i in nlist]
N = len(nlist)
print time.time()
sum1 = 0.0
sum2 = 0.0
for i in xrange(N):
	sum1 += nlist[i]
	sum2 += nlist[i]**2
mean = sum1/N
var = sum2/N - mean**2
var *= 1000000
var *= 1000000
print 'var=%10.14f'%var
import math
sd = math.sqrt(var)
print 'sd=%10.14f'%sd
print time.time()

