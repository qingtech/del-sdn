#encoding:utf-8
import gv
import sys
import error
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'

#设交换机数量为sn,则
#s_wei[sn]代表各个交换机的权重
#l_wei[sn][sn]代表链路权重
#level代表当传划分的层次,从第0层开始
def inital_partition(index,s_wei,l_wei,level):
	if level < 0 or level > gv.level:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
		
	sn = len(s_wei)
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_wei) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_wei[i]) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
		
	base = 2**level
	partition = [0+base]*sn
	if level == gv.level:
		return partition
	#get bipartition of graph

	#part 0 of bipartition
	#part 1 of bipartition
	sn0 = 0
	sn1 = 0
	for i in range(sn):
		if partition[i] == base:
			sn0 +=1
		else:
			sn1 +=1
	index_0 = [0]*sn0
	index_1 = [0]*sn1
	s_wei_0 = [0]*sn0
	s_wei_1 = [0]*sn1
	l_wei_0 = [[0]*sn0]*sn0
	l_wei_1 = [[0]*sn1]*sn1
	#index,s_wei
	i0 = 0
	i1 = 0
	for i in range(sn):
		if partition[i] == base:
			index_0[i0] = index[i]
			s_wei_0[i0] = s_wei[i]
			i0 += 1
		else:
			index_1[i1] = index[i]
			s_wei_1[i1] = s_wei[i]
			i1 += 1
	#l_wei_0
	ii = 0
	jj = 0
	for i in range(sn):
		if partition[i] == base+1:
			for j in range(sn):
				if partition[j] == base+1:
					l_wei_0[ii][jj] = l_wei_0[i][j]
					jj += 1
			ii += 1	

	#l_wei1
	ii = 0
	jj = 0
	for i in range(sn):
		if partition[i] == base:
			for j in range(sn):
				if partition[j] == base:
					l_wei_0[ii][jj] = l_wei_0[i][j]
					jj += 1
			ii += 1	
