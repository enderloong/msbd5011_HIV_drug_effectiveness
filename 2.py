# -*- coding: utf-8 -*-
"""
Created on Sun May  6 12:44:00 2018

@author: suzhi
"""

#%%
import os
#os.chdir('E:\\5011statistic\\project')
import numpy as np
import matplotlib.pyplot as plt

#%%
import csv
import pandas as pd

dirpath = os.getcwd()
datapath = os.path.join(dirpath, 'data2.csv')
data2 = pd.read_csv(datapath)

#%%
data2.dropna(inplace=True)  #无空白条目

#原有1309个用户
patients = data2['PtID']
patients = list(set(patients))

#删除只有一条记录的用户
x_dict = {}     #{ID:[CD4 date]}
y_dict = {}     #{ID:[CD4 count]-log}

for i in patients:
    x_parameter = list(data2[data2['PtID']==i]['CD4Date'])
    y_parameter = list(data2[data2['PtID']==i]['CD4Count'])
    if len(y_parameter) <=1:
        continue
    else:
        x_dict[i] = x_parameter
        y_dict[i] = y_parameter

patient = list(x_dict.keys())   #剩下1187人


#%%
def plot(ptID):
    x = np.array(x_dict[ptID])
    y = np.array(y_dict[ptID])
    xp = np.linspace(0, max(x), 500)
    m = best_m[ptID]
    plt.plot(x, y, '.', xp, m(xp), '-')
    plt.xlabel('CD4 Date')
    plt.ylabel('CD4 Count')

#%%
#x,y:np.array;
#res Residuals of the least-squares fit
#只考虑 CD4 进行回归
def reg(x,y,n):
    coef = np.polyfit(x,y,n,full = True)[0]
    res = np.polyfit(x,y,n,full = True)[1]
    model = np.poly1d(coef)
    return res,model

#%%
#防止过拟合？最高3次方，4个系数

best_res = {}
best_m = {}

for ptID in x_dict:
    x = np.array(x_dict[ptID])
    y = np.array(y_dict[ptID])
    if len(x) >= 4:
        for i in [1,2,3]:
            residuals = {}
            models = {}
            residuals[i] = reg(x,y,i)[0]
            models[i] = reg(x,y,i)[1]
        n = min(residuals)
        best_res[ptID] = min(residuals.values())
        best_m[ptID] = models[n]
    else:
        for i in [1,2]:
            residuals = {}
            models = {}
            residuals[i] = reg(x,y,i)[0]
            models[i] = reg(x,y,i)[1]
        n = min(residuals)
        best_res[ptID] = min(residuals.values())
        best_m[ptID] = models[n]
        
#%%
#取0-50周
#result {ID:[threapy,age,max-value-C0,max-value-time]}
#max-value-C0 越大越好
#max-value-time 越小越好
#0，0表示一直下降 无效
result_2 = {}     
for ptID in patient:
    pm = {}     #{xp1:yp1,}
    ans = data2.loc[data2['PtID']==ptID,['therapy']]
    therapy = int(ans.iloc[0])
    anss = data2.loc[data2['PtID']==ptID,['age']]
    age = int(anss.iloc[0])
    c0 = y_dict[ptID][0]
    #xp = np.linspace(0,50,1000)           #t,周
    #m = best_m[ptID]
    #max_cd4 = c0
    #max_t = 0
    #for x in xp:       
    #    cur_t = x
    #    cur_cd4 = m(x)
    #    if cur_cd4 > max_cd4:
    #        max_cd4 = cur_cd4
    #        max_t = x
    result_2[ptID] = [therapy,age,c0,x_dict[ptID][-1],y_dict[ptID][-1]] 
    #result_2[ptID] = [therapy,age,y_dict[ptID][-1],c0] #2显著
    #result_2[ptID] = [therapy,age,max_cd4,c0]   #1 疗效显著
    #result_2[ptID] = [therapy,age,(max_cd4-c0),c0]  #5.6疗效显著
    #result_2[ptID] = [therapy,age,(max_cd4-c0),max_t] #5.6max-t不显著
    #result_2[ptID] = [therapy,age,(max_cd4-c0)/(c0+0.0000001),max_t]
    
#%%
#将result_2变成dataframe
#new_df = pd.DataFrame(list(result_2.values()), columns=['threapy','age', 'max-increment','max-time'])

#df_1 = pd.DataFrame(columns=['therapy','age', 'max-increment','max-time'])
#df_2 = pd.DataFrame(columns=['therapy','age', 'max-increment','max-time'])
#df_3 = pd.DataFrame(columns=['therapy','age', 'max-increment','max-time'])
#df_4 = pd.DataFrame(columns=['therapy','age', 'max-increment','max-time'])

new_df = pd.DataFrame(list(result_2.values()), columns=['therapy','age','initial','last-time','last-cd4'])

df_1 = pd.DataFrame(columns=['therapy','age','initial','last-time','last-cd4'])
df_2 = pd.DataFrame(columns=['therapy','age','initial','last-time','last-cd4'])
df_3 = pd.DataFrame(columns=['therapy','age','initial','last-time','last-cd4'])
df_4 = pd.DataFrame(columns=['therapy','age','initial','last-time','last-cd4'])

for ind in range(len(new_df)):
    if new_df.iloc[ind,0]==1:
        df_1 = df_1.append(new_df.iloc[ind,:])
    elif new_df.iloc[ind,0]==2:
        df_2 = df_2.append(new_df.iloc[ind,:])
    elif new_df.iloc[ind,0]==3:
        df_3 = df_3.append(new_df.iloc[ind,:])
    elif new_df.iloc[ind,0]==4:
        df_4 = df_4.append(new_df.iloc[ind,:])
    #else:
    #    print('error')

df_1 = df_1.sort_values(by=['age'])   #294条 15-70岁
df_2 = df_2.sort_values(by=['age'])   #290条 19-66岁
df_3 = df_3.sort_values(by=['age'])   #295条 14-74岁
df_4 = df_4.sort_values(by=['age'])   #298条 15-62岁

####输出4个dataframe 分别是四类药物 按年纪排序的结果

#%%
#写成csv文件
df_1.to_csv ("df_1.csv" , index=False)
df_2.to_csv ("df_2.csv" , index=False)
df_3.to_csv ("df_3.csv" , index=False)
df_4.to_csv ("df_4.csv" , index=False)
#xxx = pd.read_csv ("df_1.csv" )

new_df.to_csv ("new_df.csv" , index=False)

#%%
#分组
a=0
b=0
c=0
d=0
dfxxx=df_4
for ind in range(len(dfxxx)):
    if dfxxx.iloc[ind,1]<=30:
        a=a+1
    elif dfxxx.iloc[ind,1]>30 and dfxxx.iloc[ind,1]<=35:
        b=b+1
    elif dfxxx.iloc[ind,1]>35 and dfxxx.iloc[ind,1]<=40:
        c=c+1
    else:
        d=d+1
    
print(a,b,c,d)    
#65 76 64 89
#61 70 70 89
#61 70 70 89
#63 81 67 97
    