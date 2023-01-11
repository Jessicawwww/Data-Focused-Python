# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 20:55:45 2021

@author: Lenovo
"""

# File: mystats.py
import numpy as np


# part (b)
#define the mean function here
def basic_mean(number1, *args):
    sum1 = number1
    num = 1
    for arg in args:
        sum1 += arg
        num += 1
    result = sum1 / num
    return result


# part (c)
def is_iter(v):
    v_is_iter = True
    try:
        iter(v)
    except:
        v_is_iter = False
    return v_is_iter


def mean(arg1, *args):
    if is_iter(arg1):
        sum2 = sum(arg1)
        num1 = len(arg1)
    else:
        sum2 = arg1
        num1 = 1
    for arg in args:
        if is_iter(arg):
            sum2 += sum(arg)
            num1 += len(arg)
        else:
            sum2 += arg
            num1 += 1
    result = sum2 / num1
    return result


# part (f)
#define the median function here
def sort(nums):
    numlist = list(nums)
    n = len(numlist)
    for i in range(n-1):
        for j in range(n-i-1):
            if numlist[j] > numlist[j+1]:
                numlist[j], numlist[j+1] = numlist[j+1], numlist[j]
    return numlist


def median(arg1, *args):
    if is_iter(arg1):
        ls = arg1
    else:
        ls = [arg1]
    for arg in args:
        ls.append(arg)
    ls1 = sort(ls)
    if len(ls) % 2 == 1:
        return ls1[len(ls1) // 2]
    else:
        return (ls1[len(ls1) // 2 - 1] + ls1[len(ls1) // 2]) / 2


if __name__ =='__main__':
    #part a
    print('The current module is:', __name__)
    # when mystats.py is the main module, the output is : The current module is: __main__
    
    #part b test
    print('mean(1) should be 1.0, and is:', basic_mean(1))
    print('mean(1,2,3,4) should be 2.5, and is:',basic_mean(1, 2, 3, 4))
    print('mean(2.4,3.1) should be 2.75, and is:',basic_mean(2.4, 3.1))
    #print('mean() should FAIL:', mean())
    
    #part c test
    print('mean([1,1,1,2]) should be 1.25, and is:', mean([1, 1, 1, 2]))
    print('mean((1,), 2, 3, [4,6]) should be 3.2,' + 'and is:', mean((1,), 2, 3, [4, 6]))
    
    #part d test
    for i in range(10):
        print("Draw", i, "from Norm(0,1):",np.random.randn())

    ls50 = [np.random.randn() for i in range(50)]
    print("Mean of", len(ls50), "values from Norm(0,1):",mean(ls50))
    ##output: Mean of 50 values from Norm(0,1): 0.15457427625031647
    
    ls10000 = [np.random.randn() for i in range(10000)]
    print("Mean of", len(ls10000), "values from Norm(0,1):",mean(ls10000))
    #output: Mean of 10000 values from Norm(0,1): -0.002573408897407548

    # part e test
    seed = 0
    np.random.seed(seed)
    a1 = np.random.randn(10)
    print("a1:", a1)  # should display an ndarray of 10 values
    print("the mean of a1 is:", mean(a1)) ##the mean of a1 is: 0.7380231707288347
    
    #part f test
    print("the median of a1 is:", median(a1))
    print("median(3, 1, 5, 9, 2):", median(3, 1, 5, 9, 2))
else:
    print("imported module is: ", __name__)
