import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import csv
import os

'''
1. Download the html code of the main pages. 
'''

def download_mainpages_html():
    # page: 1 - 4
    for i in range(4):
        url = 'https://www.yellowpages.com.au/find/supermarkets-grocery-stores/adelaide-sa-5000/page-' + str(i+1)
        print(url)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        #Write in file.
        file = open('yellowpages_page' + str(i+1) + '.txt', "wb") 
        file.write(response.content)  
        file.close()



'''
2. Scrape the html code of the main pages.
   Find all supermarkets' urls.
'''

def find_supermarkets_urls():
    #download_mainpages_html()
    
    fw = open('supermarkets_urls.txt','w')
    
    for i in range(1,5): # page: 1-4
    
        soup = BeautifulSoup(open("yellowpages_page" + str(i) + ".txt").read(),features="lxml")
        
        #for link in soup.find_all("div", class_="Box__Div-dws99b-0 bMUVdR MuiPaper-root MuiCard-root MuiPaper-elevation1 MuiPaper-rounded"):
        #    print(link)
        
        # Find supermarkets' information.
        supermarkets_divs = soup.find_all("div", class_="Box__Div-dws99b-0 bMUVdR MuiPaper-root MuiCard-root MuiPaper-elevation1 MuiPaper-rounded")
        
        print("there are", len(supermarkets_divs), "supermarkets.")
        
        for div in supermarkets_divs:
            supermarket_a = div.find_all('a', {'class': 'MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary'})
            for a in supermarket_a:
                try:
                    # Find subpages' urls (supermarkets' urls).
                    print(a['href'])
                    fw.write("https://www.yellowpages.com.au" + a['href'] + "\n")
                except KeyError:
                    pass
        
    fw.close()



'''
3. Download the html code of each subpage (supermarket).
'''

def download_subpages_html():
    #find_supermarkets_urls()
    fr = open('supermarkets_urls.txt','r')
    for url in fr:#each url
        print(url.strip())
        html = urlopen(url.strip())
        bsyc = BeautifulSoup(html.read(), "html.parser")
        #name = bsyc.find_all("a", class_="listing-name")[0].contents[0]
        #print(name)
        
        if(os.path.exists('supermarkets_html') == False):
            os.mkdir('supermarkets_html') 
            
        fw = open('supermarkets_html/' + url.split('/')[-1].split('.')[0] + '.txt','wt',encoding='utf-8')
        fw.write(str(bsyc))
        fw.close()
    
    fr.close()



'''
4. Scrape the html code of each supermarket.
   Get supermarkets' information (name, address, latitude, longitude, phone, website).
'''
def create_supermarkets_csv():
    #if you want to scrape data, uncomment following line
    #download_subpages_html()
    df_supermarkets = pd.DataFrame()
    fr = open('backupcsv/supermarkets_urls.txt','r')
    index = 1
    for url in fr:#each url
        dict_supermarket = {}
        try:
            soup = BeautifulSoup(open('supermarkets_html/' + url.split('/')[-1].split('.')[0] + '.txt','r').read(),features="lxml")
            
            # Get name
            name = soup.find_all("a", class_="listing-name")[0].contents[0]
            #print(name)
            dict_supermarket['name'] = name
            
            # Get address
            address = soup.find_all("div", class_="body left right")[0].contents[5].contents[0]
            #print(address)
            dict_supermarket['address'] = address
            
            # Get latitude
            latitude = soup.find_all("div", class_="body left right")[0].contents[5]['data-geo-latitude']
            #print(latitude)
            dict_supermarket['latitude'] = latitude
            
            #Get longitude
            longitude = soup.find_all("div", class_="body left right")[0].contents[5]['data-geo-longitude']
            #print(longitude)
            dict_supermarket['longitude'] = longitude
            
            #Get phone number
            phone = soup.find_all("div", class_="text-and-image inside-gap inside-gap-medium grow")[0].contents[3].contents[1].contents[0]
            #print(phone)
            dict_supermarket['phone'] = phone
            
            #Get website
            try:
                website = soup.find_all("a", class_="contact contact-main contact-url")[0]['href']
                #print(website)
                dict_supermarket['website'] = website
            except:
                pass
            
            # dict -> Series
            series_supermarket = pd.Series([name,address,latitude,longitude,phone,website], index=['name','address','latitude','longitude','phone','website'])
            #print(series_supermarket)
            
            # Add series to dataframe
            df_supermarkets[index] = series_supermarket
            index = index + 1
        except:
            pass
    
    fr.close()
    df_supermarkets = df_supermarkets.T
    #print(df_supermarkets)

    # save to csv
    df_supermarkets.to_csv('backupcsv/supermarkets.csv', encoding='utf-8', index=False)

'''
5. Read supermarkets' information from csv.
'''
def read_supermarkets_csv():
    create_supermarkets_csv()
    source_data = pd.read_csv("backupcsv/supermarkets.csv")
    lst = source_data.values.tolist()
    return lst








