# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 23:12:17 2021

@author: Kate
"""

import time

#open input file and four temporary output file to store result
data_path = "C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\cme.20210903.c.pa2"
output_path1 = "C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output1.txt"
output_path2 = "C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output2.txt"
output_path3 = "C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output3.txt"
output_path4 = "C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output4.txt"

fin = open(data_path, 'rt',encoding = 'utf-8')
#saving table1 
fout1 = open(output_path1, 'wt', encoding='utf-8')
fout2 = open(output_path2, 'wt', encoding='utf-8')
#saving table2
fout3 = open(output_path3, 'wt', encoding='utf-8')
fout4 = open(output_path4, 'wt', encoding='utf-8')


#write column names
fout1.writelines(['Futures Code  ', 'Contract Month  ', 'Contract Type  ','Futures Exp Date  ','Options Code  ','Options Exp Date  ','\n'])
fout1.writelines(['-----------            ','-----------            ','-----------            ','-----------            ','-----------            ','-----------            ','\n'])
fout3.writelines(['Futures Code  ', 'Contract Month  ', 'Contract Type  ','Strike Price  ','Settlement Price  ','\n'])
fout3.writelines(['-----------        ','-----------        ','-----------        ','-----------        ','-----------        ','\n'])

#scan the input file
while(True):
    line = fin.readline()
    #iterate to the last row
    if not line:
        break;
    #first table --- future
    if(line[0]=='B'and line[5:7]=='CL' and line[7]==' '):
        line_list = line.strip(' ').split(' ')
        s1 = [x for x in line_list if x!='']
        #future code
        fc = (s1[1])[3:]
        #contract month
        cm = (s1[2])[3:]
        cm_date=time.strftime('%Y-%m', time.strptime(cm,'%Y%m'))
        #set it between 2021-10 and 2023-12
        if(time.strptime(cm_date,'%Y-%m')>time.strptime('2023-12','%Y-%m')) or (time.strptime(cm_date,'%Y-%m')<time.strptime('2021-10','%Y-%m')):
            continue
        #contract type
        ct = 'Fut'
        #Futures Exp Date
        fed = (s1[3])[-10:-2]
        fed_date=time.strftime('%Y-%m-%d', time.strptime(fed,'%Y%m%d'))
        fout1.writelines([fc+'                  ',cm_date+'                  ',ct+'                  ',fed_date+'                  ','\n'])
        continue
    #first table -- options
    if(line[0]=='B' and line[5:7]=='LO' and line[7]==' '):
        line_list = line.strip(' ').split(' ')
        s1 = [x for x in line_list if x!='']
        #future code
        fc=(s1[4])[-2:]
        #contract month
        cm = (s1[2])[3:]
        cm_date=time.strftime('%Y-%m', time.strptime(cm,'%Y%m'))
        #set it between 2021-10 and 2023-12
        if(time.strptime(cm_date,'%Y-%m')>time.strptime('2023-12','%Y-%m')) or (time.strptime(cm_date,'%Y-%m')<time.strptime('2021-10','%Y-%m')):
            continue
        #contract type
        ct = 'Opt'
        #options code
        oc = (s1[1])[-2:]
        #Options Exp Date 
        oed = (s1[4])[-10:-2]
        oed_date=time.strftime('%Y-%m-%d', time.strptime(oed,'%Y%m%d'))
        fout2.writelines([fc+'                  ',cm_date+'                  ', ct+'                  ','                  ',oc+'                  ', oed_date+'                  ','\n'])
        continue
    #second table -- future
    if(line[0:2]=='81' and line[5:7]=='CL' and line[7]==' '):
        line_list = line.strip(' ').split(' ')
        s1 = [x for x in line_list if x!='']
        #future code
        fc = s1[1]
        #contract month
        cm = s1[3]
        cm_date=time.strftime('%Y-%m', time.strptime(cm,'%Y%m'))
        if(time.strptime(cm_date,'%Y-%m')>time.strptime('2023-12','%Y-%m')) or (time.strptime(cm_date,'%Y-%m')<time.strptime('2021-10','%Y-%m')):
            continue
        #type
        ct='Fut'
        #strike price
        sp=str(int((s1[4])[-16:-2])/100)
        fout3.writelines([fc+'                  ',cm_date+'                  ',ct+'                  ','                  ',sp+'                  ','\n'])
    #second table -- options
    if(line[0:2]=='81' and line[5:7]=='LO'and line[7]==' '):
        line_list = line.strip(' ').split(' ')
        s1 = [x for x in line_list if x!='']
        #future code
        fc = s1[1]
        #contract month
        cm = s1[3]
        cm_date=time.strftime('%Y-%m', time.strptime(cm,'%Y%m'))
        if(time.strptime(cm_date,'%Y-%m')>time.strptime('2023-12','%Y-%m')) or (time.strptime(cm_date,'%Y-%m')<time.strptime('2021-10','%Y-%m')):
            continue
        #call or put
        if (s1[2])[3]=='C':
            ct = 'Call'
        elif (s1[2])[3]=='P':
            ct='Put'
        #strike price
        stp = str(int((s1[4])[0:7])/100)
        #settle price
        sep=str(int((s1[4])[-16:-2])/100)
        fout4.writelines([fc+'                  ',cm_date+'                  ',ct+'                  ',stp+'                  ',sep+'                  ','\n'])

#close temp files
fout1.close()
fout2.close()
fout3.close()
fout4.close()

fout = open("C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output.txt",'a',encoding = 'utf-8')
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output1.txt','r') as f1:
    line1 = f1.read()
    fout.write(line1)
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output2.txt','r') as f2:
    line2 = f2.read()
    fout.write(line2)
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output3.txt','r') as f3:
    line3 = f3.read()
    fout.write(line3)
with open('C:\\Users\\Think\\Desktop\\21Fall课程安排\\Data Focused Python\\HW2\\output4.txt','r') as f4:
    line4 = f4.read()
    fout.write(line4)
fout.close()
        
