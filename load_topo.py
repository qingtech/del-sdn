#coding:utf-8
import sys
import gv
import error
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
def load_topo():
	#set controller number:gv.c_num
	#set switch number:gv.s_num
	#set link number:gv.l_num
	#load network topology:
	not_arg_m = 'not argument'
	not_eno_m = 'not enough argument'
	ivl_arg_m = 'invalid argument'
	
	f = open(gv.net_topo_file)
	line = f.readline()
	
	if not line:
		error.report(filename, name, frame.f_lineno, not_arg_m)

	line = line.strip('\n')
	tmp = line.split(" ")
	if(len(tmp)<3):
		error.report(filename, name, frame.f_lineno, not_eno_m)
	
	if not(tmp[0].isdigit() and tmp[1].isdigit() and tmp[2].isdigit()):
		error.report(filename, name, frame.f_lineno, ivl_arg_m)

	gv.c_num = int(tmp[0]);
	gv.s_num = int(tmp[1]);
	gv.l_num = int(tmp[2]);
	#load network topology
	sn = gv.s_num
	gv.net_topo = [[0 for col in range(sn)] for row in range(sn)]
	i = 0
	while 1:
		if i >= sn:
			break;
		line = f.readline()
		if not line:
			error.report(filename, name, frame.f_lineno, '%s\ni=%d'%(not_eno_m,i))
		line = line.strip('\n')
		tmp = line.split(' ')
		if len(tmp)<sn:
			error.report(filename, name, frame.f_lineno, '%s\ni=%d'%(not_eno_m,i))
		for j in range(sn):
			if not tmp[j].isdigit():
				error.report(filename, name, frame.f_lineno, '%s\ni=%d,j=%d'%(ivl_arg_m,i,j))
			gv.net_topo[i][j] = int(tmp[j])
		i += 1
			
			
if __name__ == '__main__':
	load_topo()
	print 'controller number: %d,'%gv.c_num,
	print 'switch number: %d,'%gv.s_num,
	print 'link number: %d'%gv.l_num
	s1 = "12"
	#print '12:%s'%s1.isdigit()
	s1 = '1.1'
	#print '1.1:%s'%s1.isdigit()
	#print isinstance('1.1',float)
	print 'network topology'
	for i in range(gv.s_num):
		for j in range(gv.s_num):
			print '%d '%gv.net_topo[i][j],
		print ' '
