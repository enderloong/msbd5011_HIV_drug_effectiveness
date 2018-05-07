ctrl = 0
if(ctrl < 1){
  data2_the1 <- read.csv(file = 'df_1.csv')
  data2_the2 <- read.csv(file = 'df_2.csv')
  data2_the3 <- read.csv(file = 'df_3.csv')
  data2_the4 <- read.csv(file = 'df_4.csv')
  data2_the <- list(the1 = data2_the1, the2 = data2_the2, the3 = data2_the3, the4 = data2_the4)
}

if(ctrl < 2){
  data_age_the <- matrix(0,4,65)
  for(i in 1:4){
    age <- data2_the[[i]]$age
    for(j in 1:length(age)){
      idx <- age[j] -10
      data_age_the[i,idx] <- data_age_the[i,idx] + 1
    }
  }
  data_cdf_age <- data_age_the
  for(i in 2:length(data_cdf_age[1,])){
    data_cdf_age[,i] = data_cdf_age[,i-1] + data_cdf_age[,i]
  }
  tpdata <- as.data.frame(t(data_cdf_age))
}

if(ctrl < -3){
  datalen <- length(tpdata[,1])
  gfig <- ggplot()
  gfig <- gfig + geom_line(data = tpdata, aes(x = 1:datalen, y = V1), colour = 'red')
  gfig <- gfig + geom_line(data = tpdata, aes(x = 1:datalen, y = V2), colour = 'green')
  gfig <- gfig + geom_line(data = tpdata, aes(x = 1:datalen, y = V3), colour = 'blue')
  gfig <- gfig + geom_line(data = tpdata, aes(x = 1:datalen, y = V4), colour = 'black')
  gfig
}

if(ctrl < 4){
  w = 1
  totallen <- c(length(data2_the1[,1]), length(data2_the2[,1]), length(data2_the3[,1]), length(data2_the4[,1]))
  data_refine <- matrix(0,sum(totallen), 3)
  for(i in 1:4){
    data_temp <- data2_the[[i]]
    firstidx <- 0
    if(i > 1){
      firstidx <- sum(totallen[1:i-1])
    }
    mi <- max(data_temp$max.increment)
    mt <- max(data_temp$max.time)
    for(j in 1:length(data_temp[,1])){
      data_refine[j+firstidx, 1] <- data_temp$threapy[j]
      if(data_temp$age[j] < 30){
        data_refine[j+firstidx, 2] <- 1
      }else if(data_temp$age[j] <35){
        data_refine[j+firstidx, 2] <- 2
      }else{
        data_refine[j+firstidx, 2] <- 3
      }
      data_refine[j+firstidx, 3] <- 0
      if(data_temp$max.time[j] > 0){
        data_refine[j+firstidx, 3] <- w * data_temp$max.increment[j]/mi + (1 - w) * mt / data_temp$max.time[j]
      }
    }
  }
}

if(ctrl < 5){
  df_refined <- as.data.frame(data_refine)
  df_refined[,1] <- factor(df_refined$V1, ordered = FALSE)
  df_refined[,2] <- factor(df_refined$V2, ordered = TRUE)
  anova_result <- aov(V3 ~ V1 * V2, data = df_refined)
}

if(ctrl < -6){
  num1 <- 0
  num2 <- 0
  num3 <- 0
  for(i in 1:4){
    data_temp <- data2_the[[i]]
    for(j in 1:length(data_temp[,1])){
      if((data_temp$max.increment[j] == 0)){
        num1 <- num1 + 1
      } 
      if((data_temp$max.time[j] == 0)){
        num2 <- num2 + 1
      } 
      if(!(data_temp$max.increment[j] == 0) && (data_temp$max.time[j] == 0)){
        num3 <- num3 + 1
      } 
    }
  }
  gfig <- ggplot()
  gfig <- gfig + geom_point(data = data2_the1, aes(x = max.increment, y = max.time))
  gfig
}