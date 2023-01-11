# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 22:23:49 2021

@author: Nel
Find nearby locations based on lattitude, longitude and types
"""

import pandas as pd
import requests, json
import re
from urllib.request import urlopen, Request 

def main(): #test module using examples
    print('Supermarket')
    print(getNearby('supermarket', '-34.9232159', '138.6088053'))
    print('Restaurant')
    print(getNearby('restaurant', '-34.9232159', '138.6088053'))
    print('Bus Stop')
    print(getNearby('bus_station', '-34.9232159', '138.6088053'))

def getNearby(types, lat, lng):
    coord = str(lat) + '%2C' + str(lng) #convert longitude and lattitude that fits google api
    headers = {'user-agent':
               "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
               } # create a header
    url ='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + coord + '&radius=1500&type=' + types+ '&key=AIzaSyDxspGstiCUAYCUIsVAgs7WRW4ftMHb9Yg'
    #call google api
    request = Request(url, headers=headers) #get response
    html = urlopen(request)
    data = html.read()
    js = json.loads(data) #read the data as json format
    name = [i['name'] for i in js['results']] #find out nearby spots' name data
    address = [i['vicinity'] for i in js['results']]# find nearby address data
    dict = {'Name': name,
            'Address': address
        } #formatting
    data = pd.DataFrame(dict) 
    return data #return formatted data
 #   print(data)

    
    
if __name__ == '__main__':
    main()

    