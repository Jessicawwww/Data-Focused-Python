# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 17:44:26 2021

@author: Kate
"""

# coding:utf-8

# import modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def crawl_news_list():
    '''
    use selenium to mock firefox for web scraping
    scrape data after storyblock is loaded
    scrape html source code
    '''
    #set FireFox driver for web scraping
    driver = webdriver.Firefox(executable_path = 'driver\geckodriver.exe')
    #set page load timeout
    driver.set_page_load_timeout(100)
    #target url
    url = 'https://www.news.com.au/search-results?q=house+rent'
    try:
        #open the url through firefox driver
        res = driver.get(url)        
    except TimeoutException:
            print("Timeout")
    #wait until html class'storyblock' loaded
    wait = WebDriverWait(driver, 120)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'storyblock')))
    
    #first 5 pages
    for i in range(5):
        #auto click next to change page
        driver.find_element_by_xpath("//a[contains(@aria-label,'Next')]").click()
        #extract all html scripts
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        file_name = 'news_html\html_source_code_'+str(i)+'.html'
        with open(file_name, 'wb+') as f:
            f.write(source_code.encode('utf-8'))
    
    driver.close()
    
if __name__ == "__main__":
    crawl_news_list()

