# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 14:54:50 2021

@author: Think
"""

###a. record list
records = []
with open("expenses.txt",'r') as f:
    for line in f:
        records.append(line.rstrip())

for line in records:
    print(line)
    

#b. use list comprehension
with open("expenses.txt",'r') as f:
    records2 = [line.rstrip() for line in f]

print("\nrecords == records2:",records == records2, '\n')
#the print result is records == records2: True 

##c. nested tuple conversion to create tuple of tuples

with open("expenses.txt",'r') as f:
    records3 = tuple([tuple(line.rstrip().split(":")) for line in f])

for tup in records3:
	print(tup)


##d. using set comprehension notation with records to create cat_set and date_set
cat_set = set()
cat_set = {line[1] for line in records3[1:] if all(line[1]!=cat for cat in cat_set)} 
date_set = set()
date_set = {line[2] for line in records3[1:] if all(line[2]!=date for date in date_set)}

print('Categories:', cat_set, '\n')
print('Dates:     ', date_set, '\n')


##e. use dict comprehension notation with records3
rec_num_to_record = dict(zip(range(len(records3)),records3))
for rn in range(len(rec_num_to_record)):
	print('{:3d}: {}'.format(rn, rec_num_to_record[rn]))

#using the items() iterable, to display rec_num_to_record:
for i in rec_num_to_record.items():
	print('{:3d}: {}'.format(i[0], i[1]))

#using tuple unpacking into two loop variables
for k, v in rec_num_to_record.items():
	print('{:3d}: {}'.format(k, v))

