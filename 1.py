# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:10:57 2018

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
datapath = os.path.join(dirpath, 'data1.csv')
data1 = pd.read_csv(datapath)

#%%
#先将dataframe割开，从而删除掉 NaN记录
da1 = data1.loc[:, ['PtID','CD4Date','CD4Count']]
da2 = data1.loc[:, ['PtID','RNADate','VLoad']]

da1.dropna(inplace=True)   #余下1662条
da2.dropna(inplace=True)   #余下1572条

#%%
#23725 第一条记录是-2

#%% get all patient ID  
#356/354 有些没记录
#patient1 = da1['PtID']
#patient1 = list(set(patient1))

#patient2 = da2['PtID']
#patient2 = list(set(patient2))

patient = data1['PtID']
patient = list(set(patient))

patient1 = da1['PtID']
patient1 = list(set(patient1))

patient2 = da2['PtID']
patient2 = list(set(patient2))


#%% 分开存 CD4和Vload
# x:CD4 date; y: CD4count
# t:RNA date; v: VLoad
x_dict = {}     #{ID:[CD4 date]}
y_dict = {}     #{ID:[CD4 count]}

t_dict={}
v_dict = {}

for i in patient:
    x_parameter = list(da1[da1['PtID']==i]['CD4Date'])
    y_parameter = list(da1[da1['PtID']==i]['CD4Count'])
    t_parameter = list(da2[da2['PtID']==i]['RNADate'])
    v_parameter = list(da2[da2['PtID']==i]['VLoad'])
    x_dict[i] = x_parameter
    y_dict[i] = y_parameter
    t_dict[i] = t_parameter
    v_dict[i] = v_parameter
    

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
##5个点 1-4次 4个点1-3次   1-（len-1）次方可以拟合 i in range(1,len)
#全部点都穿过 res=0 会过拟合吧
'''
best_res = {}
best_m = {}

for ptID in x_dict:
    x = np.array(x_dict[ptID])
    y = np.array(y_dict[ptID])
    for i in range(1,len(x)):
            residuals = {}
            models = {}
            residuals[i] = reg(x,y,i)[0]
            models[i] = reg(x,y,i)[1]
    n = min(residuals)
    best_res[ptID] = min(residuals.values())
    best_m[ptID] = models[n]
'''


#%% 
'''
result = {}     #{ptID:[终止时间]}
for ptID in x_dict:
    if ptID != 23557 and ptID != 23667:
        period = x_dict[ptID][-1]
        last_vload = v_dict[ptID][-1]
        coe = best_m[ptID].c
        if period>10 and last_vload >3:
            result[ptID] = -1
        elif len(coe) == 2 and coe[0] < 0 :
            result[ptID] = -1
        else:
            coe[-1] -= 500
            root = np.roots(coe)
            for i in root:
                if isinstance(i, complex):
                    result[ptID] = -1
                else:
                    ans = []
                    if i > 0:
                        ans.append(i)
                        result[ptID] = ans
                        print(ptID)
'''
#%%
'''
for ptID in result:
    if result[ptID] != -1:
        print(ptID,result[ptID])
'''  
#%%
#先通过Vload的最终浓度和时间 (x>10 且 y>3）时，直接放弃治疗；
#否则 转至CD4拟合预测终止治疗时间
        
result = {}     #{ptID:[终止时间]}
for ptID in patient:
    if ptID in patient2:
        last_period = t_dict[ptID][-1]
        last_vload = v_dict[ptID][-1]
        if last_period>10 and last_vload >3:
            result[ptID] = [last_period, 'stop-treatment']
            continue      
    coe = best_m[ptID].c 
    new_coe = coe.copy()
    new_coe[-1] -= 500
    root = np.roots(new_coe)
    for i in root:
       if isinstance(i, complex):
           result[ptID] = [x_dict[ptID][-1],'stop-treatment']
       else:
           ans = []
           if i > 0:
               ans.append(i)
               predtime = min(ans)
               if predtime > x_dict[ptID][-1]:
                   result[ptID] = [min(ans),'keep-treatment']
                   break
               else:
                   result[ptID] = [x_dict[ptID][-1],'stop-treatment']
           else:
               result[ptID] = [x_dict[ptID][-1],'stop-treatment']
    
            
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
for pt in result:
    lis=result[pt]
    if lis[1] != 'stop-treatment':
        print('ok',pt)

#%%
'''
纯CD4预测
ok 23580
ok 23623
ok 23662
ok 23663
ok 23665
ok 23720
ok 23721
ok 23722
ok 23763
ok 23438
ok 23481
ok 23525
ok 23529
ok 23530

23763 23525


加上Vload
ok 23580
ok 23623
ok 23662
ok 23663
ok 23665
ok 23720
ok 23721
ok 23722
ok 23438
ok 23481
ok 23529
ok 23530
'''