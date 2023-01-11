# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 18:49:34 2021
Scrape house information from domain and get geometry information
@author: Nel
"""
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
from findCoord import findCoord

def getLocation():
    '''
    source: domain, scraping website to find useful data
    '''
    headers = {'user-agent':
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
           }
    url = 'https://www.domain.com.au/rent/?excludedeposittaken=1&suburb=adelaide-sa-5000'
    res = requests.get(url = url, headers = headers)
    html = res.text
    bs = BeautifulSoup(html, 'html.parser')
    '''
    find useful data within website data by searching html attributes
    '''
    location1 = []
    location2 = []
    cost = []
    location = []
    lat = []
    lng = []
    url = []
    fts = []
    feature = []
    price = []
    l1 = bs.findAll(attrs = {"data-testid": "address-line1"}) #find address1 html elements
    l2 = bs.findAll(attrs = {"data-testid": "address-line2"}) #find address2 elements
    ct = bs.findAll(attrs = {"data-testid": "listing-card-price"}) #find price
    ft = bs.findAll(attrs = {"data-testid": "property-features-text-container"}) #find features
    href = bs.findAll('a', 'address is-two-lines css-1y2bib4') #find url elements
    for t in href:
        url.append(t.get("href")) #find url data
    for t in l1:#formatting address1 data
        location1.append(re.sub('<[^<]+?>', '', str(t)).replace('\n', '').strip())
    for t in l2:#address2 format
        location2.append(re.sub('<[^<]+?>', '', str(t)).replace('\n', '').strip())
    for t in ct:#formatting price
        cost.append(re.sub('<[^<]+?>', '', str(t)).replace('\n', '').strip())
    for t in ft: #formatting features
        string = re.sub('<[^<]+?>', '', str(t)).replace('\n', '').strip()
        st = re.sub('−', '0', str(string))
        fts.append(re.sub('\..*}', '', str(st)))
    for i in range(len(location1)): #merge address1 and address2
        location.append(location1[i] + location2[i])
    for i in range(int(len(fts)/3)):# each house has three features so need to merge each 3
        feature.append(fts[3*i] + ', ' + fts[3*i+1] + ', ' + fts[3*i+2])
    for t in cost:
        price.append(float("".join(re.findall(r"\d+\.?\d*", t))))
    for i in location: #find geometry information by using address
        latti, longi = findCoord(i)
        lat.append(latti)
        lng.append(longi)
    name = ['']*len(location) #formatting with data from other source
    source = ['domain']*len(location) #provide source information
    rating = ['']*len(location) #cross-source format
    dict = {'location': location, 
            'prices': price,
            'features': feature,
            'listing_url': url,
            'name': name,
            'lat': lat,
            'long': lng,
            'source': source,
            'rating': rating
            } #formatting all dara
    data = pd.DataFrame(dict)
    print(data)
    path = 'backupcsv\rental_listings.csv'
    data.to_csv(path, sep=',', index = False, header = False, mode = 'a', encoding = 'utf_8_sig') #extract data to csv file
    return data
        
if __name__ == '__main__': #test function
    getLocation()