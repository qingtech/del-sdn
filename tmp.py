#功能求出交换机index从src_part_no转移到dst_part_no后的gain
#输入：index,src_part_no,dst_part_no,part,s_wei,l_wei,src_sw_1,src_sw_2,dst_sw_1,dst_sw_2,src_pq,dst_pq,gain
#输出：src_sw_1,src_sw_2,dst_sw_1,dst_sw_2
def get_gain(index,src_part_no,dst_part_no,part,s_wei,l_wei,src_sw_1,src_sw_2,dst_sw_1,dst_sw_2,src_pq = None,dst_pq = None,gain = None)
	'''
	#检查转移交换机index是否会使两个分区的交换机权重更加不平衡
	#暂时将交换机index转移到另一个分区
	if part[index] == lc_part_no:
		part[index] = rc_part_no
	else:
		part[index] = lc_part_no

	tmp_s_wei_2 = get_s_wei_2(s_wei, l_wei, part)
	tmp_lc_sum_sw = get_sum_s_wei_by_part(s_wei, part, lc_part_no) + get_sum_s_wei_by_part(tmp_s_wei_2, part, lc_part_no)
	tmp_rc_sum_sw = get_sum_s_wei_by_part(s_wei, part, rc_part_no) + get_sum_s_wei_by_part(tmp_s_wei_2, part, rc_part_no)
	#将交换机index转回到原分区
	if part[index] == lc_part_no:
		part[index] = rc_part_no
	else:
		part[index] = lc_part_no
	#########################################################
	'''
	if part[index] == src_part_no:
		################
		src_sw_1 -= s_wei[index]
		dst_sw_1 += s_wei[index]
		################
	else:
		################
		src_sw_1 += s_wei[index]
		dst_sw_1 -= s_wei[index]
		################
	#重新调整与交换机index相邻的交换机的gain
	for j in xrange(sn):
		if j == index:
			continue
		if part[index] == src_part_no:
			if part[j] == src_part_no:
				########################
				dst_sw_2 += l_wei[j][index]
				src_sw_2 += l_wei[index][j]
				########################
				#必须乘以2,囧。。。2BUG
				gain[j] += (l_wei[index][j] + l_wei[j][index])*2
				if not check[j]:
					src_pq.update(gain[j], j)
			else:
				########################
				src_sw_2 -= l_wei[j][index]
				dst_sw_2 -= l_wei[index][j]
				########################
				gain[j] -= (l_wei[index][j] + l_wei[j][index])*2
				if not check[j]:
					dst_pq.update(gain[j], j)
		else:
			if part[j] == src_part_no:
				########################
				dst_sw_2 -= l_wei[j][index]
				src_sw_2 -= l_wei[index][j]
				########################
				gain[j] -= (l_wei[index][j] + l_wei[j][index])*2
				if not check[j]:
					src_pq.update(gain[j], j)
			else:
				s_wei_2[index] += l_wei[j][index]
				s_wei_2[j] += l_wei[index][j]
				lc_sum_sw += l_wei[j][index]
				rc_sum_sw += l_wei[index][j]
				########################
				src_sw_2 += l_wei[j][index]
				dst_sw_2 += l_wei[index][j]
				########################
				gain[j] += (l_wei[index][j] + l_wei[j][index])*2
				if not check[j]:
					dst_pq.update(gain[j], j)
	################################################################
