# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 20:46:10 2021

@author: Lenovo
"""

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import news_crawler2
import news_crawler1

def crawl_news():
    '''
    crawl news from website
    extract news' title, url, intro, keyword, date
    store the data in output.csv file
    '''
    #scrape news list
    news_crawler1.crawl_news_list()
    #extract title and url for each news
    news_crawler2.extract_from_html()
    
    #read file of each news' title and url
    data = pd.read_csv('backupcsv\index.csv', encoding = 'utf_8_sig')
    
    #select only news from www.news.au.com
    #others need subscription
    url_list_ori = data['url']
    url_list = []
    for url in url_list_ori:
        if url[:16] == "https://www.news":
            url_list.append(url)
    
    #create list for stoing data
    keyword_list=[]
    date_list = []
    headline_list = []
    intro_list = []
    
    #use firefox driver for scraping
    driver = webdriver.Firefox(executable_path = 'driver\geckodriver.exe')
    #set page load time out
    driver.set_page_load_timeout(100)
    
    #scrape each news url
    for url in url_list:
        try:
            #start the firefox to open the url
            res = driver.get(url)        
        except TimeoutException:
            print("Timeout")
        #wait until the html class'site-content' loaded
        wait = WebDriverWait(driver, 120)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'site-content')))
        
        #extract element from html id and add element into lists
        elem_date = driver.find_element_by_id("publish-date").text
        date_list.append(elem_date)
        elem_headline = driver.find_element_by_id("story-headline").text
        headline_list.append(elem_headline)
        elem_intro = driver.find_element_by_id("story-intro").text
        intro_list.append(elem_intro)
        elem_keyword = driver.find_element_by_xpath("//meta[@name='keywords']").get_attribute("content")
        keyword_list.append(elem_keyword)
    
    driver.close()
    
    #savve the lists to output.csv file
    output = pd.DataFrame({'url':url_list, 'healine':headline_list, 'date':date_list, 'intro':intro_list, 'keyword':keyword_list})
    output.to_csv('backupcsv\news_output.csv', index=None, encoding = 'utf_8_sig')    

if __name__ == "__main__":
    crawl_news()