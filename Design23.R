ctrl <- 0
if(ctrl < 1){
  new_df <- read.csv(file = 'new_df.csv')
}

if(ctrl < 2){
  df_refined <- new_df
  df_refined$threapy <- factor(df_refined$threapy, ordered = FALSE)
  mi <- rep(1,4)
  for(i in 1:4){
    mi[i] <- max(df_refined$max.increment[df_refined$threapy == i])
  }
  for(j in 1:length(df_refined$max.increment)){
    df_refined$max.increment[j] <- df_refined$max.increment[j]/mi[df_refined$threapy[j]]
  }
}

if(ctrl < 3){
  anova_result <- aov(max.increment ~ threapy * age * initial, data = df_refined)
  summary(anova_result)
}