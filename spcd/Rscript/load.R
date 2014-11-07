#Input:load.txt

#1.从文件里读取区域负载
    #列:algs,topo,kway,part,scount,load,sd,sd2
    #e.g.
#setwd('d://')
load = read.table('load.txt',header=TRUE,sep="\t")
#2. 计算区域负载标准差
std = load
#delete column part
std = std[,-4]
#delete column scount
std = std[,-4]
#delete column load
std = std[,-4]
#delete column sd
std = std[,-4]
#delete column sd2
std = std[,-4]
#remove duplicated
std = std[which(!duplicated(std)),]

for(i in 1:length(std$algs)){
  a = as.character(std$algs[i])
  t = as.character(std$topo[i])
  k = as.character(std$kway[i])
  l = load[load$algs==a & load$topo==t & load$kway==k,]
  std$std[i] = sd(l$load)
}
#3. 画出区域负载标准差图
require(ggplot2)
std$kway = factor(std$kway)
############################################
qplot(kway,std, data=std, fill=algs, facets = topo ~ .,
      xlab='k-way', ylab='domain load standard deviation',
      geom='bar', position='dodge', stat='identity',)
ggsave('standard_deviation_of_domain_load.pdf')


# gsub<-ggplot(std, aes(x=kway, y=std, fill=algs, alpha=topo),)
# plotg<-gsub+geom_bar(stat="identity",position=position_dodge(width=0.9))
# plotg <- plotg + xlab("k-way")
# plotg <- plotg + ylab('domain load standard deviation')
# plotg <- plotg + ylim(0,10)
# print(plotg)
# ############################################
# topo = std$topo
# topo = topo[which(!duplicated(topo))]
# for(i in 1:length(topo)){
#   s = std[std$topo==topo[i],]
#   gsub<-ggplot(s, aes(x=kway, y=std, colour=algs, shape=algs,),)
#   plotg<-gsub+geom_bar(stat="identity",position=position_dodge(width=0.9,), fill='white',)
#   plotg<-plotg+geom_point(position=position_dodge(width=0.9), size=7)
#   plotg <- plotg + labs(title=topo[i])
#   plotg <- plotg + xlab("k-way")
#   plotg <- plotg + ylab('domain load standard deviation')
#   plotg <- plotg + ylim(0,10)
#   #plotg <- plotg + title('topo')
#   file_name = paste('load_standard_deviation_by_',topo[i],'.pdf',sep='')
#   #print(file_name)
#   ggsave(file_name)
#   print(plotg)
# }

