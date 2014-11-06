#Input:load.txt

#1.从文件里读取区域负载
#列:algs,topo,kway,part,scount,load
#e.g.
#setwd('d://')
traffic = read.table('traffic.txt',header=TRUE,sep="\t")


#2. 画出区域负载标准差图
require(ggplot2)
traffic$kway = factor(traffic$kway)
############################################
qplot(kway,traffic/flow, data=traffic, fill=algs, facets = topo ~ .,
      xlab='k-way', ylab='inter-domain traffic',
      geom='bar', position='dodge', stat='identity',)
ggsave('inter_domain_traffic.pdf')

