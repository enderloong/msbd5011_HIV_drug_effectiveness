ctrl <- 0
if(ctrl < 1){
  new_df <- read.csv(file = 'new_df.csv')
}

if(ctrl < 2){
  df_refined <- new_df
  df_refined$therapy <- factor(df_refined$therapy, ordered = FALSE)
  ml <- rep(1,4)
}

if(ctrl < 3){
  anova_result <- aov( last.cd4 ~ therapy + age + initial, data = df_refined)
  summary(anova_result)
}