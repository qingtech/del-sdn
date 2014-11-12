#Input:load.txt

#1.从文件里读取区域负载
#列:algs,topo,kway,part,scount,load,sd,sd2
#e.g.
#setwd('d://')
load = read.table('load.txt',header=TRUE,sep="\t")


#2. 画出区域负载标准差图
require(ggplot2)
load$kway = factor(load$kway)
############################################
qplot(kway,sd, data=load, fill=algs, facets = topo ~ .,
      xlab='number of domain', ylab='standard deviation of domain load',
      geom='bar', position='dodge', stat='identity',)
ggsave('standard_deviation_of_domain_load1.pdf')
qplot(kway,sd2, data=load, fill=algs, facets = topo ~ .,
      xlab='number of domain', ylab='standard deviation of domain load',
      geom='bar', position='dodge', stat='identity',)
ggsave('standard_deviation_of_domain_load2.pdf')

