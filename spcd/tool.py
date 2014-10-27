#encoding=utf-8

#功能：根据链路权重l_wei将中间路径建立请求添加到s_wei
#输入：
#l_wei: 链路权重
#输出：
#s_wei_2: 中间路径建立请求
def get_s_wei_2(l_wei, part):
	sn = len(l_wei)
	#数据合法性检验
	assert sn > 0
	for i in range(sn):
		assert len(l_wei[i]) == sn
	assert len(part) == sn

	#算法开始
	s_wei_2 = [0]*sn
	for i in range(sn-1):
		for j in range(i+1,sn):
			if part[i] != part[j]:
				s_wei_2[i] += l_wei[j][i]
				s_wei_2[j] += l_wei[i][j]
	return s_wei_2

#功能：获得分区号为c_part_no的分区子网络
#输入：s_swei[],s_wei_2[],l_wei[][],part,c_part_no
#输出：分区子网络_net_topo[c_s_wei[],c_l_wei[]],对应父网络的交换机编号c_index[]
def get_child_network(s_wei,s_wei_2,l_wei,l_lan,part,c_part_no):
	sn = len(s_wei)
	#数据合法性检验
	assert sn > 0
	assert len(l_wei) == sn
	for i in range(sn):
		assert len(l_wei[i]) == sn
	assert len(part) == sn

	#算法开始	

	#统计分区交换机个数
	c_s_num = 0
	for i in range(sn):
		if part[i] == c_part_no:
			c_s_num +=1
	#如果不存在该分区子网络
	if c_s_num == 0:
		return None
	c_index = [0]*c_s_num
	c_s_wei = [0]*c_s_num
	c_l_wei = [[0 for col in xrange(c_s_num)] for row in xrange(c_s_num)]
	c_l_lan = [[0 for col in xrange(c_s_num)] for row in xrange(c_s_num)]

	#what a f*cking bug 囧。。。。。
	#c_l_wei = [[0]*c_s_num]*c_s_num

	#index,s_wei
	ii = 0
	for i in xrange(sn):
		if part[i] == c_part_no:
			c_index[ii] = i
			c_s_wei[ii] = s_wei[i] + s_wei_2[i]
			ii += 1
	#复杂度：O(switch_number^2)
	#c_l_wei
	for i in xrange(c_s_num):
		ii = c_index[i]
		for j in xrange(c_s_num):
			jj = c_index[j]
			c_l_wei[i][j] = l_wei[ii][jj]
			c_l_lan[i][j] = l_lan[ii][jj]
	res = [c_s_wei,c_l_wei,c_l_lan,c_index]
	return res

#输入:分区结果partition, 控制器放置结果ctr_place, s_wei, l_wei, l_lan
#输出:区域交换机数part_s_num, 区域负载part_s_wei, 跨域流量edge_cut,
def get_res(s_wei, l_wei, l_lan, partition, ctr_place):

	sn = len(s_wei)
	part_s_num = {}
	part_s_wei   = {}
	s_wei_2 = get_s_wei_2(l_wei, partition)
	edge_cut = 0
	edge_not_cut = 0	#edge_not_cut = sum(l_wei) - edge_cut
	for i in range(sn):
		edge_cut += s_wei_2[i]
	for i in xrange(sn):
		for j in xrange(sn):
			edge_not_cut += l_wei[i][j]
	edge_not_cut -= edge_cut

	for i in range(sn):
		part_s_num[partition[i]] = 0
		part_s_wei[partition[i]] = 0
	for i in range(sn):
		part_s_num[partition[i]] += 1
		part_s_wei[partition[i]] += s_wei[i] + s_wei_2[i]

	#获取part_no
	part_no = {}
	for i in range(sn):
		part_no[partition[i]] = partition[i]
	part_cost = {}
	
	'''
	for c_part_no in part_no.keys():
		res = get_child_network(s_wei,s_wei_2,l_wei,l_lan,partition,c_part_no)
		if res == None:
			ctr_place[c_part_no-pn] = -1
			part_cost[c_part_no-pn] = 0
			continue
			
		c_s_wei = res[0]
		c_l_wei = res[1]
		c_l_lan = res[2]
		c_index = res[3]
		res = controller_deployment(c_s_wei,c_l_wei,c_l_lan)
		ctr_i = res[0]
		ctr_place[c_part_no-pn] = c_index[ctr_i]
		part_cost[c_part_no-pn] = res[1]
	'''

	return [part_s_num, part_s_wei, edge_cut, part_cost]


