from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##Part A 
html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2020')

bsyc = BeautifulSoup(html.read(), "lxml")
'''
fout = open('bsyc_temp.txt', 'wt',
		encoding='utf-8')

fout.write(str(bsyc))

fout.close()

# print the first table
#print(str(bsyc.table))
# ... not the one we want


# so get a list of all table tags
table_list = bsyc.findAll('table')

# how many are there? 8
print('there are', len(table_list), 'table tags')

# look at the first 50 chars of each table
for t in table_list:
    print(str(t)[:50])
    
'''
# only one class="t-chart" table, so add that
# to findAll as a dictionary attribute
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )
'''
# how many are there? 1
print(len(tc_table_list), 't-chart tables')
'''
# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# initiate outpit 2D list
daily_yield_curves = []

#set row and colum index
row=0
col=0

#set list header
daily_yield_curves.append(['Date', '1 mo', '2 mo', '3 mo', '6 mo', '1 yr', '2 yr',
 '3 yr', '5 yr', '7 yr', '10 yr', '20 yr', '30 yr'])

#append tc_table's contents into 2D list
for c in tc_table.children:
    if row == 0:
        row+=1
        continue
    daily_yield_curves.append([])
    for r in c.children:
        if col!=0:
            daily_yield_curves[row].append('%.2f'%float(r.contents[0]))
        else:
            daily_yield_curves[row].append(r.contents[0])
        col+=1
    col=0
    row+=1

print(daily_yield_curves)

#write to txt output
with open('daily_yield_curves.txt','w') as f:
    for i in daily_yield_curves:
        f.write(str(i))
        f.write('\n')
'''
# what are this table's components/children?
for c in tc_table.children:
    print(str(c)[:50])

# tag tr means table row, containing table data
# what are the children of those rows?
for c in tc_table.children:
    for r in c.children:
        print(str(r)[:50])

# we have found the table data!
# just get the contents of each cell
for c in tc_table.children:
    for r in c.children:
        print(r.contents)
'''
##Part B
from matplotlib import cm
from matplotlib.pyplot import MultipleLocator

trading_days = [i for i in range(len(daily_yield_curves[1:]))]
month_to_maturity = [1,2,3,6,12,24,36,60,84,120,240,360]

#calculate XYZ for surface plot
X =  np.array([[i]*len(month_to_maturity) for i in trading_days])
Y = month_to_maturity*len(trading_days)
Y = np.reshape(Y, (251, 12))
Z =[i[1:] for i in daily_yield_curves[1:]]
Z = np.array(Z)
Z = Z.astype(np.float64)
X = X.astype(np.int32)
Y = Y.astype(np.int32)

#set figure size
fig = plt.figure()
fig.set_size_inches(18.5,15,forward=True)

#add subplot
ax1 = fig.add_subplot(2,1,1, projection='3d')
ax2 = fig.add_subplot(2,1,2, projection='3d')
ax1.plot_surface(X, Y, Z,cmap=cm.coolwarm,linewidth=0, antialiased=False)
ax2.plot_wireframe(X, Y, Z)

#set colorbar for surface plot
color1 = ax1.plot_surface(X, Y, Z,cmap=cm.coolwarm,linewidth=0, antialiased=False)
position=fig.add_axes([0.68,0.65,0.02,0.12])
fig.colorbar(color1, cax=position, shrink=0.5, aspect=5)

#set axis scale
x_major_locator=MultipleLocator(25)
ax1.xaxis.set_major_locator(x_major_locator)
y_major_locator=MultipleLocator(50)
ax1.yaxis.set_major_locator(y_major_locator)
z_major_locator=MultipleLocator(0.5)
ax1.zaxis.set_major_locator(z_major_locator)

ax2.xaxis.set_major_locator(x_major_locator)
ax2.yaxis.set_major_locator(y_major_locator)
ax2.zaxis.set_major_locator(z_major_locator)

#set axis label names and title
ax1.set_xlabel('trading days since 01/02/20')
ax1.set_ylabel('months to maturity')
ax1.set_zlabel('rate')
ax1.set_title("Surface plot")

ax2.set_xlabel('trading days since 01/02/20')
ax2.set_ylabel('months to maturity')
ax2.set_zlabel('rate')
ax2.set_title("Wireframe plot")

plt.show()

##Part C
##set the index and column names
cols_name = daily_yield_curves[0][1:]
index_name = [i[0] for i in daily_yield_curves[1:]]
#item
content_list = [i[1:] for i in daily_yield_curves[1:]]
yield_curve_df = pd.DataFrame(content_list,index = index_name,columns = cols_name)
#convert datatype from object to float
for col in cols_name:
    yield_curve_df[col] = pd.to_numeric(yield_curve_df[col],errors='coerce')
print(yield_curve_df.info())
#plot 1st data frame
yield_curve_df.plot(title="Interest Rate Time Series, 2020")
#slice the data frame and transpose it
new_index_name = [1,2,3,6,12,24,36,60,84,120,240,360]

by_day_yield_curve_df = yield_curve_df.iloc[range(0,len(yield_curve_df),20)].T
by_day_yield_curve_df.index = new_index_name
#plot 2nd data frame
by_day_yield_curve_df.plot(title = "2020 Yield Curves, 20 Day Intervls",xticks = range(0,360,50),
                           xlim=(0,350),yticks = [i/100 for i in range(0,250,25)],ylim= (0.0,2.5))
