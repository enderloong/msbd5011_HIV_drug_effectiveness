require(ggplot2)

#Pts_reccnt <- as.data.frame(table(data1$PtID))
#Pts_preproc <- Pts_reccnt[Pts_reccnt$Freq > 3,]
datalen <- length(data1$PtID)

Pts_1 <- matrix(0, 356, 5)
for(i in 1:356){
  Pts_id <- Pts[i]
  Pts_info <- as.matrix(data1[data1$PtID == Pts_id,])
  Pts_1[i,1:5] <- Pts_info[1,1:5]
}
ptid = Pts_1[Pts_1[,3] < 20,1]
Cd4_1_id <- rep(FALSE, datalen)
for(j in 1:121){
  Cd4_1_id[data1$PtID == ptid[j]] = TRUE
}
Cd4_1 <- data1[Cd4_1_id,]
# plot(Cd4_1$CD4Date, Cd4_1$CD4Count)

rcid <- as.integer(runif(40,1,356))


tp_id <- rep(FALSE, datalen)
for(i in 1:length(rcid)){
  tp_id[data1$PtID == Pts[rcid[i]]] = TRUE
}
tpdata <- data1[tp_id,]
gfig <- ggplot()
for(i in 1:length(rcid)){
  figdata = data1[data1$PtID == Pts[rcid[i]],]
  gfig <- gfig + geom_line(data = figdata,aes(x = RNADate, y=VLoad))
}
gfig