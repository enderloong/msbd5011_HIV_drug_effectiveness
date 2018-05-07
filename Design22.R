ctrl = 3
if(ctrl < 1){
  data2_the1 <- read.csv(file = 'df_1.csv')
  data2_the2 <- read.csv(file = 'df_2.csv')
  data2_the3 <- read.csv(file = 'df_3.csv')
  data2_the4 <- read.csv(file = 'df_4.csv')
  data2_the <- list(the1 = data2_the1, the2 = data2_the2, the3 = data2_the3, the4 = data2_the4)
}

if(ctrl < 4){
  totallen <- c(length(data2_the1[,1]), length(data2_the2[,1]), length(data2_the3[,1]), length(data2_the4[,1]))
  data_refine <- matrix(0,sum(totallen), 4)
  for(i in 1:4){
    data_temp <- data2_the[[i]]
    firstidx <- 0
    if(i > 1){
      firstidx <- sum(totallen[1:i-1])
    }
    mi <- max(data_temp$max.increment)
    for(j in 1:length(data_temp[,1])){
      data_refine[j+firstidx, 1] <- data_temp$threapy[j]
      data_refine[j+firstidx, 2] <- data_temp$age[j]
      data_refine[j+firstidx, 3] <- data_temp$initial[j]
      data_refine[j+firstidx, 4] <- data_temp$max.increment[j]/mi
    }
  }
}
if(ctrl < 5){
  df_refined <- as.data.frame(data_refine)
  df_refined[,1] <- factor(df_refined$V1, ordered = FALSE)
  anova_result <- aov(V4 ~ V1 + V3, data = df_refined)
  summary.aov(anova_result)
}