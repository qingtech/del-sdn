#encoding=utf-8
import gv
import error
import sys
import copy
frame = sys._getframe()
filename = sys._getframe().f_code.co_filename
name = sys._getframe().f_code.co_name
not_arg_m = 'not argument'
not_eno_m = 'not enough argument'
ivl_arg_m = 'invalid argument'

#功能；在所有交换机中选取一个交换机与控制器直接相连，使得控制器与交换机的通讯总体花费最少
#输入：
#s_wei[i]表示交换机i需要与交换机进行通讯（包括流建立请求和转发规则下发）的次数
#l_lan[i][j]表示该链路的“距离”，交换机与控制器的通讯总是走“距离”最短的路径，使用Floyd算法得到
#输出：
#i：与控制器直接相连的交换机
def controller_place(s_wei,l_wei,l_lan):
	#数据合法性检验
	sn = len(s_wei)
	if sn < 0:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	if len(l_lan) != sn:
		error.report(filename, name, frame.f_lineno, ivl_arg_m)
	for i in range(sn):
		if len(l_lan[i]) != sn:
			error.report(filename, name, frame.f_lineno, ivl_arg_m)
	#算法开始
	#每个交换机和控制器通讯的次数（流建立请求，规则下发）
	com_num = [0]*sn
	for i in xrange(sn):
		#流建立请求（包括回应）
		com_num[i] = s_wei[i]*2
		for j in xrange(sn):
			#规则建立部分
			com_num[i] += l_wei[j][i]
	#Floyd最短路径
	map = copy.deepcopy(l_lan)
	for i in range(sn):
		for j in range(sn):
			for k in range(sn):
				if map[i][k] + map[k][j] < map[i][j]:
					map[i][j] = map[i][k] + map[k][j]
	cost = sys.maxint
	ii = -1
	for i in range(sn):
		tmp_cost = 0
		for j in range(sn):
			tmp_cost += com_num[j]*map[i][j]
		if tmp_cost < cost:
			ii = i
			cost = tmp_cost
	#最短路径矩阵
	print '最短路径矩阵：'
	for i in range(sn):
		for j in range(sn):
			print '%d '%map[i][j],
		print ''
	print '通讯总花费：%d'%cost 
	return ii
if __name__ == '__main__':
	max = 10000
	"""
		     (1) (1)
		(2)1————0————2(10)
		     	|
			|(1)
		     	|
		     	3(2)
	"""
	s_wei = [2,2,10,2]
	l_lan = [[0,1,1,1],[1,0,max,max],[1,max,0,max],[1,max,max,0]]
	l_wei = [[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0]]
	i = controller_place(s_wei,l_wei, l_lan)
	print 'i=%d'%i
