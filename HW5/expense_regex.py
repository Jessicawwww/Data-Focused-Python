# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 22:46:46 2021

"""
import re

#a
records=[]
f = open("expenses.txt", encoding = 'utf-8')
while True:
    line = f.readline()
    if(line):
        records.append(line)
    else:
        break
f.close()
    
pat=r'D'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)


#b contain a single quote (') character
pat=r'\''
for line in records:
    if(re.search(pat,line)!=None):
        print(line)


#c contain a double quote (") character
pat = r'\"'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)


#d begin with 7
pat = r'^7'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)


#e end with an r or a t
pat = r'r$|t$'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)


#f contain a literal period (.) character
pat = r'\.'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)



#g contain an r followed later by a g.  
# (The r and the g do not need to be consecutive characters.)
pat=r'r.*g'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)

#h contain two consecutive uppercase letters (for example, AA, DF, LM, YW, …).
pat = r'[A-Z][A-Z]'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)

#i.	contain a comma (,) character.
pat = r','
for line in records:
    if(re.search(pat,line)!=None):
        print(line)

#j.	contain three or more comma characters (not necessarily consecutive).
pat = r',.*,.*,.*,*'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)
        
#k.	do not contain any v, w, x, y, or z characters.
pat = r'^[^vwxyz]*$'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)
        
#l.	contain money amounts between 10.00 and 99.99.  
#Hint: What must the first character be (i.e. between which numbers)?  
#What must the second character be?  
#What must the third character be?  And so forth.  
pat = r'[0-9]+\.[0-9]+'
for line in records:
    if(re.search(pat,line)!=None):
        match = re.search(pat,line)
        amount = float(match.group(0))
        if 10.00<=amount<=99.99:
            print(line)


#m.	contain exactly three commas.
pat = r'^[^,]*(,)[^,]*\1[^,]*\1[^,]*$'
for line in records:
    if(re.search(pat,line)!=None):
        print(line)

#n contain a (character 
pat='\('
for line in records:
    if re.search(pat,line)!=None:
        print(line)
        
#o. describe meals costing at least 100.00.
##method1:
pat = r'[0-9]+\.[0-9]+.*meal.*'
for line in records:
    if re.search(pat,line)!=None:
        match = re.search(r'[0-9]+\.[0-9]+', line)
        amount = float(match.group(0))
        if amount>=100.0:
            print(line)
#method2:
for line in records[1:]:
    a=re.split(':',line)
    if (float(a[0])>=100.00)&(a[1]=='meal'):
        print(line)

#p have an expense category that is exactly four characters wide 
#(your pattern should work even if more lines are added to the file, with new categories that have not yet been defined). 
for line in records[1:]:
    a=re.split(':',line)
    if len(a[1])==4:
        print(line)

#q expenses that occurred in March.
for line in records[1:]:
    a=re.split(':',line)
    if a[2][4:6]=='03':
        print(line)

#r  contain an a, followed by a b, followed by a c (perhaps with other characters between the a and the b and the c).
pat=r'a.*b.*c'
for line in records:
    if re.search(pat,line)!=None:
        print(line)

#s contain some sequence of two characters, followed later by that same sequence of two characters, followed later by that same sequence of two characters again. 
pat=r'(..).*\1.*\1'
for line in records:
    if re.search(pat,line)!=None:
        print(line)

