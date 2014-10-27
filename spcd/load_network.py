#coding:utf-8
import sys
import gv
import re

def load_topo():
	#set switch number:gv.s_num
	#load network topology:
	
	f = open(gv.net_topo_file_name)
	line = f.readline()
	
	assert line

	line = line.strip('\n')

	assert line.isdigit()

	gv.s_num = int(line);

	#load network topology
	sn = gv.s_num
	gv.net_topo = [[0 for col in range(sn)] for row in range(sn)]
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
			gv.net_topo[i][j] = int(tmp[j])
		i += 1
	f.close()
			
			
if __name__ == '__main__':
	'''
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
	'''
