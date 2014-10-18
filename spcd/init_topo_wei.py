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
#输入:链路距离矩阵link_dist
#输出:后驱矩阵path_succ(successor),路径花费矩阵path_cost
def floyd(link_dist):
	infinite = sys.maxint/2;
	sn = len(link_dist)
	path_succ = [[-1 for col in xrange(sn)] for row in xrange(sn)]
	path_cost= [[infinite for col in xrange(sn)] for row in xrange(sn)]
	for i in xrange(sn):
		path_succ[i][i] = i
		path_cost[i][i] = 0

	for k in xrange(sn):
		for i in xrange(sn):
			for j in xrange(sn):
				if path_cost[i][j] > path_cost[i][k] + path_cost[k][j]
					path_succ[i][j] = path_succ[i][k]
					path_cost = path_cost[i][k] + path_cost[k][j]
	return [path_succ,path_cost]
#输入:网络拓扑矩阵net_topo(gv.net_topo),链路延迟矩阵l_lan(gv.l_lan)网络流量矩阵net_traf(gv.net_traf)
#输出:交换机权重s_wei(gv.s_wei),链路权重l_wei(gv.l_wei)
#简述:网络流量矩阵存储着任一交换机i到任一交换机j的流的数量,假设net_traf[i][j]=2,表示交换机i-->j的流
#     的数量为2,则交换机i需要向控制器发出2个流建立请求,所以s_wei[i]=2,流i-->j根据网络拓扑和链路延迟
#     计算出花费最少的路径(利用Floyd算法求出所有点到点的最短路径),假设为(i-->k-->j),则l_wei[i][k]+=2,l_wei[k][j]+=2
def init_topo_weight():
	#gv.s_wei
	#gv.l_wei

	net_topo = gv.net_topo
	l_lan = gv.l_lan
	net_traf = gv.net_traf
	sn = gv.s_num
	if sn <= 0:
		error.report(filename, name, frame.f_lineno, not_ini_m)

	s_wei = [0 for col in range(sn)]	
	l_wei = [[0 for col in range(sn)] for row in range(sn)]

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
	
