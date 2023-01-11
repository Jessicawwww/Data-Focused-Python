# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:33:59 2021

@author: Think
"""
import time
import pandas as pd



##df and df2 to store the standardized table

df = pd.DataFrame(columns = ["Futures Code","Contract Month","Contract Type","Futures Exp Date","Options Code","Options Exp Date"])

df2 = pd.DataFrame(columns = ["Futures Code","Contract Month","Contract Type","Strike Price","Settlement Price"])

# Reading the data inside the pa2 file and add content to data frames
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\cme.20210903.c.pa2', 'r') as f:
    #read the first line
    line = f.readline()  
    num = 0
    while line:
        ##table 1: start with B, product code is CL, and FUT or OOF
        try:
            if line.startswith('B') and (line[5:7]=='CL' or line[5:7]=='LO')  \
            and (line[15:18] =='FUT' or line[15:18]=='OOF') \
            and (time.strptime('202110','%Y%m')<=time.strptime(line[18:24],'%Y%m')<=time.strptime('202312','%Y%m'))\
            and line[7]==' ':
                #assign values to each field
                fcode = 'CL'
                #time format
                contract_month = time.strftime('%Y-%m',time.strptime(line[18:24],'%Y%m'))
                #FUT/OOF
                if line[15:18] =='FUT':
                    contract_type = 'Fut'
                    future_exp_date = time.strftime('%Y-%m-%d',time.strptime(line[91:99],'%Y%m%d'))
                    option_exp_date = None
                    ocode = None
                elif line[15:18] =='OOF':
                    contract_type = 'Opt'
                    future_exp_date = None
                    option_exp_date = time.strftime('%Y-%m-%d',time.strptime(line[91:99],'%Y%m%d'))
                    ocode = 'LO'
                if future_exp_date == '2021-09-20' or future_exp_date == '2021-10-19':
                    print(line)
                ##append the data to dataframe
                df=df.append(pd.DataFrame({'Futures Code':[fcode],
                                           'Contract Month':[contract_month],
                                           'Contract Type':[contract_type],
                                           'Futures Exp Date':[future_exp_date],
                                           'Options Code':[ocode],
                                           'Options Exp Date':[option_exp_date]
                                           }),ignore_index=True)
                
            #table2 : start with 81, product code is CL, FUT/OOF
            if line.startswith('81') and (line[5:7]=='CL' or line[5:7]=='LO')\
                and (line[25:28]=='FUT' or line[25:28]=='OOF') \
                and time.strptime('202110','%Y%m')<=time.strptime(line[29:35],'%Y%m')<=time.strptime('202312','%Y%m') \
                and line[7]==' ':
                fcode = 'CL'
                contract_month = time.strftime('%Y-%m',time.strptime(line[29:35],'%Y%m'))
                if line[25:28]=='FUT':
                    contract_type = 'Fut'
                    strike_price = None
                    settle_price = int(line[-16:-2])/100     
                elif line[25:28]=='OOF':
                    if line[28]=='C':
                        contract_type = 'Call'
                        strike_price = int(line[47:54])/100
                        settle_price = int(line[-16:-2])/100
                    elif line[28]=='P':
                        contract_type = 'Put'
                        strike_price = int(line[47:54])/100
                        settle_price = int(line[-16:-2])/100
                #append the data to df2
                df2=df2.append(pd.DataFrame({'Futures Code':[fcode],
                                           'Contract Month':[contract_month],
                                           'Contract Type':[contract_type],
                                           'Strike Price':[strike_price],
                                           'Settlement Price':[settle_price]
                                           }),ignore_index=True)
        except:
                print(line)
        line = f.readline()

df.to_csv('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output_v1.txt',sep='\t',index=False)
df2.to_csv('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output_v2.txt',sep='\t',index=False)

fout = open("C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output_v1.txt",'a',encoding = 'utf-8')
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output_v2.txt','r') as f1:
    line1 = f1.read()
    fout.write(line1)
fout.close()
        
    


