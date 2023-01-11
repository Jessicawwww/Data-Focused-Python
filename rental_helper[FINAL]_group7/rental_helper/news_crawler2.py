# -*- coding: utf-8 -*-

"""
Created on Wed Nov 24 18:33:37 2021

@author: Lenovo
"""

from bs4 import BeautifulSoup
import pandas as pd
import os

def extract_from_html():
    '''
    extract url and title from 5 html source code
    '''
    #create lists for storing title and url
    title_list =[]
    url_list=[]
    
    #5 html source code
    for i in range(5):
        file_name = 'news_html\html_source_code_'+str(i)+'.html'
        #open html with beautifulsoup
        soup = BeautifulSoup(open(file_name, encoding = 'utf-8'),features='lxml')
        #find storyblock_title_link_block
        rs = soup.find_all("a",class_='storyblock_title_link')
        #add title and url to list
        for a in rs:
            title_list.append(a.get_text())
            url_list.append(a.get('href'))
    
    #save lists to csv file
    data = pd.DataFrame({'url':url_list, 'title':title_list})
    data.to_csv('backupcsv\index.csv', index=None, encoding = 'utf_8_sig')
    
    #delete previous source code
    for i in range(5):
        file_name = 'html_source_code_'+str(i)+'.html'
        os.remove(file_name)
    
if __name__ == "__main__":
    extract_from_html()