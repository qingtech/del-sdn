#coding:utf-8
import sys
import gv
import error
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_ini_m = 'not initial argument'
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'
def load_topo_weight():
	#gv.c_wei
	#gv.s_wei
	#gv.l_wei
	f = open(gv.topo_wei_file)
	#load controller weight

	#load switch weight:gv.s_wei
	sn = gv.s_num
	if sn <= 0:
		error.report(filename, name, frame.f_lineno, not_ini_m)
	gv.s_wei = [0 for col in range(sn)]	
	line = f.readline()
	if not line:
		error.report(filename, name, frame.f_lineno, not_arg_m)
	line = line.strip('\n')
	tmp = line.split(" ")
	if(len(tmp)<sn):
		error.report(filename, name, frame.f_lineno, not_eno_m)
	for i in range(sn):
		if not tmp[i].isdigit():
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
		gv.s_wei[i] = int(tmp[i])

	#load weight:gv.l_wei
	gv.l_wei = [[0 for col in range(sn)] for row in range(sn)]
	i = 0
	while 1:
		if i>= sn:
			break
		line = f.readline()
		if not line:
			error.report(filename, name, frame.f_lineno, '%s\ni=%d'%(not_eno_m,i))
		line = line.strip('\n')
		tmp = line.split(' ')
		if len(tmp) < sn:
			error.report(filename, name, frame.f_lineno, '%s\ni=%d'%(not_eno_m,i))
		for j  in range(sn):
			if not tmp[j].isdigit():
				error.report(filename, name, frame.f_lineno, '%s\ni=%d,j=%d'%(not_eno_m,i,j))
			gv.l_wei[i][j] = int(tmp[j])
		i += 1
if __name__ == '__main__':
	load_topo_weight()
	sn = gv.s_num
	print 'switch weight:'
	for i in range(sn):
		print '%d '%gv.s_wei[i],
	print ''

	print 'link weight:'
	for i in range(sn):
		for j in range(sn):
			print '%d '%gv.l_wei[i][j],
		print ''
	
