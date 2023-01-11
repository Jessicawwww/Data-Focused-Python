# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 20:25:31 2021

@author: Jingyi Wu
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import findCoord
import getLocation
'''
This method is for scraping rental listings data from website: 
Homely: https://www.homely.com.au/for-rent/adelaide-sa-5000/real-estate"
Airbnb: https://zh.airbnb.com/s/Adelaide/homes?refinement_paths%5B%5D=%2Fhomes&screen_size=large

Here we use selenium driver to simulate open the url and get info
since we use a proxy/vpn here, the web loading can be slow, we set loading timeout and sleep time for javascipt to be fully loaded
But it is still not solved.
For airbnb and homely, we all need to operate it manually on each page, openning inspection to successfully scrape the webpage
we use class name to get each element and construct a dataframe

For cleaning dataframe part,
we format the price datatype and coordinate the price unit to be per week, etc.
In addition, we used google map API to get latitude and longtitude of every listing's location.
This could take a long time.

At last, we merged two dataset to be rental listings data. 
To save time for the UI part, I am gonna directly import csv data instead of going through whole scraping process. 
'''

def getHomelyListings(root_url):
    #store scraping results
    url_list = []
    price_list = []
    location_list = []
    features_list = []
    count=0
    #start selenium 
    ser = Service("driver\chromedriver.exe") 
    op = webdriver.ChromeOptions()
    s = webdriver.Chrome(service=ser, options=op)
    s.set_page_load_timeout(60)
    for num in range(1,8,1):
        current_url = root_url+"/page-"+str(num)
        s.get(current_url)
        time.sleep(1) 
        
        #WebDriverWait(s, 30).until(EC.url_changes(current_url))

        rent_list = s.find_elements(By.CLASS_NAME ,"tyvapw-0.ljrubD")
        print(len(rent_list))
        for l in rent_list:
            url = l.find_element(By.TAG_NAME,"a").get_attribute("href")
            price = l.find_element(By.CSS_SELECTOR,"h3.sc-1e63uev-3.lgaCcU").text#//h3[@class='sc-1e63uev-3.lgaCcU'] 
            location = l.find_element(By.CSS_SELECTOR,"h2.ijsdcd-1.cttOnC").text
            features = l.find_element(By.CSS_SELECTOR,"ul.rkh7f0-0.eLJGMB").text
            features = features.split("\n")

            url_list.append(url)
            price_list.append(price)
            location_list.append(location)
            features_list.append(features)
            count+=1
    
    homely_df = pd.DataFrame({
    'location':location_list,
    'price':price_list,
    'features':features_list,
    'url':url_list
    })
    print(len(url_list),len(price_list),len(location_list),len(features_list),count)
    return homely_df


def clean_homely_data(df):
    df.rename(columns={'features':'features(bed/Bath/Car)'}, inplace=True)
    #deal with price column
    df['price'] = df['price'].apply(lambda x:x.replace('$', ''))
    df['price'] = df['price'].str.extract('(\d+)', expand=False).fillna(-1).astype(int)
    
    location = list(df['location'])
    latt = []
    long = []
    for i in location:
        lat, lng = findCoord.findCoord(i)
        latt.append(lat)
        long.append(lng)
    print(len(latt),len(long))
    df['lat'] = latt
    df['long'] = long
    for feature in df['features(bed/Bath/Car)']:
        feature[0] = "Bed: "+feature[0]
        feature[1] = "Bath: "+feature[1]
        feature[2] = "Car: "+feature[2]
    
    source_list = ['homely' for i in range(len(df))]
    rating_list = ['' for i in range(len(df))]
    name_list = ['' for i in range(len(df))]
    homely_df = pd.DataFrame({
    'location':df['location'],
    'price':df['price'],
    'features':df['features(bed/Bath/Car)'],
    'listing_url':df['url'],
    'name':name_list,
    'lat':df['lat'],
    'long':df['long'],
    'source':source_list,
    'rating':rating_list
    })
    homely_df.to_csv("backupcsv\homely_data.csv",index=False,encoding = 'utf_8_sig')
    return homely_df


def getAirbnb_listing(test_url):
    ref_links = []
    rating_lists = []
    price_lists = []
    features_lists = []
    location_lists = []
    name_lists = []
    
    ser = Service("driver\chromedriver.exe")
    op = webdriver.ChromeOptions()
    s = webdriver.Chrome(service=ser, options=op)
    s.set_page_load_timeout(60)
    s.get(test_url)
    time.sleep(20)
    
    elems = s.find_elements(By.CSS_SELECTOR,"._8s3ctt [href]")
    links = [elem.get_attribute('href') for elem in elems]
    print(len(links))
    for i in range(0,40,2):
        ref_links.append(links[i])
    rent_list = s.find_elements(By.CSS_SELECTOR ,'div._12oal24')
    print(len(rent_list))
    for item in rent_list:
        #find tag
        try:
            location_tag = item.find_element(By.CSS_SELECTOR,'div._1xzimiid')
            location_tag = location_tag.text
        except:
            location_tag = ""
        location_lists.append(location_tag)
        #find name
        name = item.find_element(By.CSS_SELECTOR,'span._im5s6sq')
        name = name.text      
        name_lists.append(name)
        #find price
        price1 = item.find_element(By.CSS_SELECTOR,'span._tyxjp1')
        price1 = price1.text
        
        price2 = item.find_element(By.CSS_SELECTOR,'span._1vylq8i')
        price2 = price2.text
        price = price1+price2
        price_lists.append(price)
        
        feature_list = item.find_elements(By.CSS_SELECTOR,'span._3hmsj')
        features = [f.text for f in feature_list]
        features_lists.append(features)
        #feature = feature.text
        #_3hmsj
        #_18khxk1
        try:
            rating = item.find_element(By.CSS_SELECTOR,'span._18khxk1')
            rating = rating.text
        except:
            rating = "rating"
        rating_lists.append(rating)
        #print(location_tag,"---",name,"---",price,"---",features,"---",rating)
    for i in range(14):
        s.find_element_by_xpath("//a[contains(@aria-label,'Next')]").click()
        time.sleep(20)
        elems = s.find_elements(By.CSS_SELECTOR,"._8s3ctt [href]")
        links = [elem.get_attribute('href') for elem in elems]
        print(len(links))
        for i in range(0,40,2):
            ref_links.append(links[i])
        rent_list = s.find_elements(By.CSS_SELECTOR ,'div._12oal24')
        print(len(rent_list))
        for item in rent_list:
            #find tag
            try:
                location_tag = item.find_element(By.CSS_SELECTOR,'div._1xzimiid')
                location_tag = location_tag.text
            except:
                location_tag = ""
            location_lists.append(location_tag)
            #find name
            name = item.find_element(By.CSS_SELECTOR,'span._im5s6sq')
            name = name.text      
            name_lists.append(name)
            #find price
            price1 = item.find_element(By.CSS_SELECTOR,'span._tyxjp1')
            price1 = price1.text
            
            price2 = item.find_element(By.CSS_SELECTOR,'span._1vylq8i')
            price2 = price2.text
            price = price1+price2
            price_lists.append(price)
            
            feature_list = item.find_elements(By.CSS_SELECTOR,'span._3hmsj')
            features = [f.text for f in feature_list]
            features_lists.append(features)
            #feature = feature.text
            #_3hmsj
            #_18khxk1
            try:
                rating = item.find_element(By.CSS_SELECTOR,'span._18khxk1')
                rating = rating.text
            except:
                rating = "rating"
            rating_lists.append(rating)
        
    print(len(ref_links),len(rating_lists),len(price_lists),len(features_lists),len(location_lists),len(name_lists))
    airbnb_df = pd.DataFrame({
    'name':name_lists,
    'location_tag':location_lists,
    'features':features_lists,
    'price':price_lists,
    'rating':rating_lists,
    'listing_url':ref_links
    })
    return airbnb_df

def clean_airbnb_data(airbnb_df):
    airbnb_df['rating'] = airbnb_df['rating'].apply(lambda x:x.replace('\n', ''))
    airbnb_df[['price_number','price_unit']] = airbnb_df.price.str.split("/",expand=True,)
    airbnb_df['price_number'].astype(str)
    airbnb_df['price_number'][:20] = airbnb_df['price_number'][:20].apply(lambda x:x.replace('$', ''))
    airbnb_df['price_number'][20:] = airbnb_df['price_number'][20:].apply(lambda x:x.replace('￥', ''))
    airbnb_df['price_number'] = airbnb_df['price_number'].apply(lambda x:x.replace(',', ''))
    airbnb_df['price_number'] = pd.to_numeric(airbnb_df['price_number'], errors='coerce').convert_dtypes()
    airbnb_df['price_number'] = airbnb_df['price_number'].astype(float)
    airbnb_df[20:]['price_number'] = airbnb_df[20:]['price_number']/6.39
    
    df2 = airbnb_df.drop(columns = ['price','price_unit'])
    df2.to_csv("airbnb_cleaned_data.csv",encoding='utf_8_sig',index = False)
    
    df2['location'] = df2['location_tag'].str.split(" in ",expand=True)[1]
    airbnb_df = df2[['location','price_number','features','listing_url','name']]
    airbnb_df['location'] =[ i+", Adelaide" for i in airbnb_df['location']]
    airbnb_df['price_number'] = airbnb_df['price_number'].map(lambda x: x*7)
    
    location2 = list(airbnb_df['location'])
    latt2 = []
    long2 = []
    for i in location2:
        lat, lng = findCoord.findCoord(i)
        latt2.append(lat)
        long2.append(lng)
        #print(lat, lng)
    airbnb_df['lat'] = latt2
    airbnb_df['long'] = long2
    
    airbnb_df.rename(columns={'price_number':'price'}, inplace=True)
    airbnb_df['source'] = 'aribnb'
    airbnb_df['rating'] = df2['rating']
    
    airbnb_df.to_csv("backupcsv\airbnb_data.csv",index=False,encoding = 'utf_8_sig')
    return airbnb_df

def get_rental_data():
    root_url = 'https://www.homely.com.au/for-rent/adelaide-sa-5000/real-estate'
    df_homely = getHomelyListings(root_url)
    homely_df = clean_homely_data(df_homely)
    
    airbnb_url = 'https://www.airbnb.com/s/adelaide/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=december&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query&locale=en'
    df_airbnb = getAirbnb_listing(airbnb_url)
    airbnb_df = clean_airbnb_data(df_airbnb)
    
    rental_data = homely_df
    rental_data = rental_data.append(airbnb_df)
    rental_data.to_csv("backupcsv\rental_listings.csv",index=False,encoding = 'utf_8_sig')
    rental_data = rental_data.append(getLocation())
    return rental_data


def main():
    get_rental_data()

if __name__ == '__main__':
    main()