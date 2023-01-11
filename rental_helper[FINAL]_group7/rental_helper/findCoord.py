# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 14:07:59 2021
Get geometry information(lattitude, longitude) by using address
@author: Nel
"""
import pandas as pd
import requests, json
import re
from urllib.request import urlopen, Request 

def main():
    #test function
    location = ['5 Florey Place,ADELAIDE SA 5000',
                'C17/18 Bewes Street,ADELAIDE SA 5000',
                '15/261 Pirie Street,ADELAIDE SA 5000',
                '1303/180 Morphett Street,ADELAIDE SA 5000',
                '415/281-286 North Terrace,ADELAIDE SA 5000',
                '64 Corryton  Street,ADELAIDE SA 5000',
                '5 Florey Place,ADELAIDE SA 5000'
                '10/9 Ebenezer Place,ADELAIDE SA 5000'
                '20/107 Grote  Street,ADELAIDE SA 5000',
                '1607/15 Austin Street,ADELAIDE SA 5000',
                '28/26 Charlick Circuit,ADELAIDE SA 5000',
                '1205/15-19 Synagogue  Place,ADELAIDE SA 5000',
                '112/227 North Terrace,ADELAIDE SA 5000',
                '203/31 Frew Street,ADELAIDE SA 5000',
                '16 Heaslip Close,ADELAIDE SA 5000',
                '104/293 Angas Street,ADELAIDE SA 5000',
                '8D/17 Eden Street,ADELAIDE SA 5000',
                '208/39 Grenfell Street,ADELAIDE SA 5000',
                '6/29-31 Compton Street,ADELAIDE SA 5000',
                '1/15 Vincent Place,ADELAIDE SA 5000',
                '1206/156 Wright  Street,ADELAIDE SA 5000']
    latt = []
    long = []
    for i in location:
        lat, lng = findCoord(i)
        latt.append(lat)
        long.append(lng)
        print(lat, lng)
    data = pd.DataFrame({'Latitude': latt, 'Longitude': long}) #formatting data
    data.to_csv('getLocation.csv', sep=',', index = False, header = True) #extract data to .csv
    
def findCoord(address):
    address = address.replace(" ", "+") #format address to adapt google api url
    headers = {'user-agent':
           "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
           } #create headers
    url ='https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=AIzaSyDxspGstiCUAYCUIsVAgs7WRW4ftMHb9Yg'
    #form url to access google api
    request = Request(url, headers=headers)
    html = urlopen(request)
    data = html.read()
    js = json.loads(data) #read json format data
    lat = js['results'][0]['geometry']['location']['lat'] #find lattitude
    lng = js['results'][0]['geometry']['location']['lng'] #find longitude
    return lat, lng

if __name__ == '__main__':
    main()