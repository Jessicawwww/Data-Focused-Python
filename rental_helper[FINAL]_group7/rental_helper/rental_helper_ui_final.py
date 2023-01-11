# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 09:54:37 2021

@author: Lenovo
"""
import csv
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk


import pandas as pd
import numpy as np

import news_wordcloud #generate news keyword word cloud
import findCoord #convert address to latitude and longitude through GppgleAPI
import getNearby #get an address' nearby restaurant/bus-station/supermarket from GoogleAPI
import restaurant_crawler #crawler for restaurant data
import bus
import news_crawler3 #crawler for news data
import rental_data_crawler #crawler for houselist data on homely.com and airbnb.com
import getLocation #crawler for houselist data on domain.com

from supermarket import read_supermarkets_csv #crawler supermarket data

#root window
root = Tk()

def create_treeview(source_data, tree):
    '''
    insert source_data by line into the treebox
    '''
    
    #convert dataframe to list
    lst = source_data.values.tolist()
    table = []
    
    #convert the list into 2d list
    for row in lst:
        #for column in total_columns:
        new_row = []
        new_row.append(row[0])
        new_row.append(row[1])
        table.append(new_row)
        
    # add data to the treeview
    for row in table:
        tree.insert('', END, values=row)
        
    
def create_housedetail_window(house_name,house_address,house_price,house_features,house_link,house_source,house_rating):
    detail_window = Toplevel()
    detail_window.title('House Detail')
    #detail_window.resizable(0,0)
    detail_window.geometry('800x600')
    
    detail_window.columnconfigure(0, weight=1)
    detail_window.columnconfigure(1, weight=1)
    detail_window.columnconfigure(2, weight=3)
    detail_window.columnconfigure(3, weight=1)
    
    detail_window.rowconfigure(0,weight=1)
    detail_window.rowconfigure(1,weight=2)
    detail_window.rowconfigure(2,weight=1)
    detail_window.rowconfigure(3,weight=1)
    detail_window.rowconfigure(4,weight=1)
    detail_window.rowconfigure(5,weight=1)
    detail_window.rowconfigure(6,weight=1)
    detail_window.rowconfigure(7,weight=1)
    
    
    #convert house address to latitude and longitude
    house_lat, house_lng = findCoord.findCoord(house_address)
    #print(house_lat, house_lng)
    
    Label(detail_window, text = 'Detail Information', font=('Arial Bold', 20), pady=5, padx=5).grid(row=0,column=0, columnspan=2)
    
    Label(detail_window, text = 'Name:', font=('Bold', 10), pady=5, padx=5).grid(row=1,column=0)
    label_id = Label(detail_window, text=house_name, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_id.grid(row=1, column=1)

    Label(detail_window, text = 'Address:', font=('Bold', 10), pady=5, padx=5).grid(row=2,column=0)
    label_address = Label(detail_window, text=house_address, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_address.grid(row=2, column=1)
 
    
    Label(detail_window, text = 'Price (per week):', font=('Bold', 10), pady=5, padx=5).grid(row=3,column=0)
    label_date = Label(detail_window, text=house_price, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_date.grid(row=3, column=1)
    
    Label(detail_window, text = 'Features:', font=('Bold', 10), pady=5, padx=5).grid(row=4,column=0)
    label_cost = Label(detail_window, text=house_features, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_cost.grid(row=4, column=1)
    
    Label(detail_window, text = 'Link:', font=('Bold', 10), pady=5, padx=5).grid(row=5,column=0)
    label_link = Label(detail_window, text=house_link, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_link.grid(row=5, column=1)
    
    Label(detail_window, text = 'Source:', font=('Bold', 10), pady=5, padx=5).grid(row=6,column=0)
    label_rate = Label(detail_window, text=house_source, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_rate.grid(row=6, column=1)
    
    Label(detail_window, text = 'Rating:', font=('Bold', 10), pady=5, padx=5).grid(row=7,column=0)
    label_des = Label(detail_window, text=house_rating, font=('Bold', 10), pady=5, padx=5,wraplength=100)
    label_des.grid(row=7, column=1)
      
    #display nearby information
    #nearby busstop
    Label(detail_window, text = 'Nearby Bus-stop', font=('Arial Bold', 10), pady=5, padx=5).grid(row=0,column=2)
    #get nearbuy busstop's information
    nearby_bs_df = getNearby.getNearby('bus_station', house_lat, house_lng)
    # define columns
    columns = ('Name', 'Address')
    # create treeview
    bs_tree = ttk.Treeview(detail_window, columns=columns, show='headings',height=5)
    # define headings
    bs_tree.heading('Name', text='Name')
    bs_tree.heading('Address', text='Address')
    #add data into the tree
    create_treeview(nearby_bs_df, bs_tree)
    bs_tree.grid(column=2, row=1)
    
 
    #nearby supermarket
    Label(detail_window, text = 'Nearby Supermarket', font=('Arial Bold', 10), pady=5, padx=5).grid(row=2,column=2)
    sm_tree = ttk.Treeview(detail_window, columns=columns, show='headings',height=5)
    sm_tree.heading('Name', text='Name')
    sm_tree.heading('Address', text='Address')
    nearby_sm_df = getNearby.getNearby('supermarket', house_lat, house_lng)
    create_treeview(nearby_sm_df, sm_tree)
    sm_tree.grid(column=2, row=3, rowspan=2)
    
    #nearby restaurant
    Label(detail_window, text = 'Nearby Restaurant', font=('Arial Bold', 10), pady=5, padx=5).grid(row=5,column=2)
    rs_tree = ttk.Treeview(detail_window, columns=columns, show='headings',height=10)
    rs_tree.heading('Name', text='Name')
    rs_tree.heading('Address', text='Address')
    nearby_rs_df = getNearby.getNearby('restaurant', house_lat, house_lng)
    create_treeview(nearby_rs_df, rs_tree)
    rs_tree.grid(column=2, row=6, rowspan=2)

    #add scrollbar to each treeview
    bs_scrollbar = Scrollbar(detail_window)
    bs_scrollbar.grid(row=1, column=3)
    bs_tree.configure(yscrollcommand=bs_scrollbar.set)
    bs_scrollbar.configure(command=bs_tree.yview)
    
    sm_scrollbar = Scrollbar(detail_window)
    sm_scrollbar.grid(row=3, column=3, rowspan=2)
    sm_tree.configure(yscrollcommand=sm_scrollbar.set)
    sm_scrollbar.configure(command=sm_tree.yview)
    
    rs_scrollbar = Scrollbar(detail_window)
    rs_scrollbar.grid(row=6, column=3, rowspan=2)
    rs_tree.configure(yscrollcommand=rs_scrollbar.set)
    rs_scrollbar.configure(command=rs_tree.yview)
  

def create_houselist_window():
    '''
    display all housing resource before filtering
    display filter for price range
    display housing resource after filtering
    search house by house id
    provide entry for house detail
    '''
    
    #create new window
    houselist_window = Toplevel(root)
    houselist_window.title('House List')
    #houselist_window.resizable(0, 0)
    houselist_window.geometry('800x600')
    
    #set the layout of the window
    houselist_window.columnconfigure(0, weight=1)
    houselist_window.columnconfigure(1, weight=6)
    houselist_window.columnconfigure(2, weight=1)
    
    houselist_window.rowconfigure(0,weight=1)
    houselist_window.rowconfigure(1, weight=2)
    houselist_window.rowconfigure(2, weight=1)
    houselist_window.rowconfigure(3, weight=2)
    houselist_window.rowconfigure(4, weight=1)
    houselist_window.rowconfigure(5, weight=1)
    
    #set title label
    Label(houselist_window, text = 'Search Results', font=('Arial Bold', 24), pady=5, padx=5).grid(row=0,column=0, columnspan=2)

    #set min and max budget input entry for filter
    Label(houselist_window, text = 'min budget', font=('Arial Bold', 12), pady=5, padx=5).grid(row=1,column=0)
    min_budget_text = StringVar()
    min_budget_entry=Entry(houselist_window, textvariable = min_budget_text, width=10)
    min_budget_entry.grid(row=2, column =0)
    
    Label(houselist_window, text = 'max budget', font=('Arial Bold', 12), pady=5, padx=5).grid(row=3,column=0)
    max_budget_text = StringVar()
    max_budget_entry=Entry(houselist_window, textvariable = max_budget_text, width=10)
    max_budget_entry.grid(row=4, column =0)
    
    
    #create table for display house list
    columns = ('location','price','features','listing_url','name','source','rating')

    tree = ttk.Treeview(houselist_window, columns=columns, show='headings',height=20)
    tree.grid(row=1, column=1, sticky='nsew')
    
    # define headings
    tree.heading('location', text='location')
    tree.heading('price', text='price')
    tree.heading('features', text='features')
    tree.heading('listing_url', text='listing_url')
    tree.heading('name', text='name')
    tree.heading('source', text='source')
    tree.heading('rating', text='rating')
    
    tree.column("location",anchor=CENTER, stretch=NO, width=100)
    tree.column("price",anchor=CENTER, stretch=NO, width=100)
    tree.column("features",anchor=CENTER, stretch=NO, width=100)
    tree.column("listing_url",anchor=CENTER, stretch=NO, width=100)
    tree.column("name",anchor=CENTER, stretch=NO, width=100)
    tree.column("source",anchor=CENTER, stretch=NO, width=100)
    tree.column("rating",anchor=CENTER, stretch=NO, width=100)
    
    
    def delButton(tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)
    
    def selectItem(a):
        curItem = tree.focus()
        cont = tree.item(curItem)
        house_name = cont['values'][4]
        house_address= cont['values'][0]
        house_price = cont['values'][1]
        house_features = cont['values'][2]
        house_link = cont['values'][3]
        house_source = cont['values'][5]
        house_rating = cont['values'][6]
        print(cont['values'])
        print(type(cont['values']))
        #create search button
        search_btn = Button(houselist_window, text='Search', font=('Arial', 10), width=10, command=lambda: create_housedetail_window(house_name,house_address,house_price,house_features,house_link,house_source,house_rating))
        search_btn.grid(row=5, column=2)

    def show_table_in_window():
        min_budget =  0.0 if len(min_budget_text.get())==0 else float(min_budget_text.get())
        max_budget = 0.0 if len(max_budget_text.get())==0 else float(max_budget_text.get())
        delButton(tree)
        #insert table data
        
        #crawler for homely and airbnb
        #if you want to crawl data, uncomment following line and comment the second line
        #rental_data = rental_data_crawler.get_rental_data()
        
        rental_data = pd.read_csv("backupcsv/rental_listings.csv")
        
        lst = rental_data.values.tolist()
        table = []
        # new table
        print(min_budget,max_budget)
        for row in lst:
            if max_budget!=0.0 and min_budget<=row[1]<=max_budget:
                #for column in total_columns:
                new_row = [] #'location','price','features','listing_url','name','source','rating'
                new_row.append(row[0]) #'location'
                new_row.append(row[1]) #'price'
                new_row.append(row[2]) #'features'
                new_row.append(row[3]) #'listing_url'
                new_row.append(row[4]) #'name'
                new_row.append(row[7]) #'source'
                new_row.append(row[8]) #'rating'
                table.append(new_row)
            elif max_budget==0.0 and min_budget<=row[1]:
                new_row = [] #'location','price','features','listing_url','name','source','rating'
                new_row.append(row[0]) #'location'
                new_row.append(row[1]) #'price'
                new_row.append(row[2]) #'features'
                new_row.append(row[3]) #'listing_url'
                new_row.append(row[4]) #'name'
                new_row.append(row[7]) #'source'
                new_row.append(row[8]) #'rating'
                table.append(new_row)
            
        contacts = table
        # add data to the treeview
        for contact in contacts:
            tree.insert('', END, values=contact)
        
        #search detailed info window by curse
        tree.bind('<ButtonRelease-1>', selectItem) #return a list here

    show_table_in_window()
    #create refresh button
    refresh_btn = Button(houselist_window, text='Refresh', font=('Arial', 10), width=10, command=show_table_in_window)
    refresh_btn.grid(row=5, column=1)

    
    
def create_news_window():
    '''
    display news
    news list for most recent 10
    news keyword cloud image
    '''
    
    #create new window
    news_window=Toplevel(root)
    news_window.title('Recent News')
    #news_window.resizable(0, 0)
    news_window.geometry('800x600')
    
    #set the layout of news window
    news_window.columnconfigure(0, weight=2)
    news_window.columnconfigure(1, weight=1)
    news_window.columnconfigure(2, weight=3)
    
    news_window.rowconfigure(0,weight=1)
    news_window.rowconfigure(1, weight=1)
    news_window.rowconfigure(2, weight=1)
    news_window.rowconfigure(3, weight=1)
    news_window.rowconfigure(4, weight=3)
    news_window.rowconfigure(5, weight=1)
    
    #titles for two parts
    Label(news_window, text = 'Recent News', font=('Arial Bold', 12), pady=5, padx=5).grid(row=0,column=0)
    Label(news_window, text = 'Selected News Detail', font=('Arial Bold', 12), pady=5, padx=5).grid(row=0,column=1, columnspan=2)
    Label(news_window, text = 'Recent News Keywords', font=('Arial Bold', 12), pady=5, padx=5).grid(row=5,column=1, columnspan=2)
    
    #create news list table
    #list_font = tkFont.Font(family = 'Helvetica',size=10)
    news_list = Listbox(news_window, width=50, height=30, border=0)
    news_list.grid(row=1, column=0, rowspan=4)
    
    #show news detail
    def show_news_detail():
        index = news_list.curselection()[0]
        title_text.config(text = data[index][1])
        link_text.config(text = data[index][0])
        intro_text.config(text = data[index][3])
    
    #button for news detail
    detail_news_button = Button(news_window, text="See detail news", command=show_news_detail)
    detail_news_button.grid(row=5, column=0)
    
    #labels of detail news
    Label(news_window, text = 'News Title', font=('Bold', 10), pady=5, padx=5).grid(row=1,column=1)
    title_text = Label(news_window, text='not specifed', font=('Bold',10), pady=5, padx=5, wraplength=100)
    title_text.grid(row=1, column=2)
    Label(news_window, text = 'News Link', font=('Bold', 10), pady=5, padx=5).grid(row=2,column=1)
    link_text = Label(news_window, text='not specifed', font=('Bold',10), pady=5, padx=5, wraplength=100)
    link_text.grid(row=2, column=2)
    Label(news_window, text = 'News Intro', font=('Bold', 10), pady=5, padx=5).grid(row=3,column=1)
    intro_text = Label(news_window, text='not specifed', font=('Bold',10), pady=5, padx=5, wraplength=100)
    intro_text.grid(row=3, column=2)
    
    #if you want to scrape data, uncomment following line
    #news_crawler3.crawl_news()
    
    #insert data title into newslist
    #file = open(
        #r"../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/86cf176018a02243e8e2dfdfaf9513ae/Message/MessageTemp/3c7ee09f21558ddc06641c369359cfa4/File/news_output.csv", encoding='utf-8')

    file = open(r"backupcsv/news_output.csv", encoding ='utf-8')
    reader = csv.reader(file)
    data = list(reader)

    list_of_entries = []
    for x in range(30):
        list_of_entries.append(data[x][1])

    for x, y in enumerate(list_of_entries):
        news_list.insert(x, y)
    
    
    news_wordcloud.generate_keyword_cloud()
    #create image and add image into a label
    keyword_img = Image.open('backupcsv/keyword_cloud.png')
    keyword_img = keyword_img.resize((200,200), Image.ADAPTIVE)
    keyword_img = ImageTk.PhotoImage(keyword_img)
    img_label = Label(news_window, image = keyword_img, pady=10, padx=10)
    img_label.image = keyword_img
    img_label.grid(row=4, column=1, columnspan=2)

def create_restaurant_window():
    '''
    display restaurant in adelaide
    display detail information of selected item
    '''
    # create new window
    detail_window = Toplevel()
    detail_window.title('Restaurants in Adelaide')
    #detail_window.resizable(0, 0)
    detail_window.geometry('800x600')

    # set the layout of restaurant window
    detail_window.columnconfigure(0, weight=1)
    detail_window.columnconfigure(1, weight=1)
    detail_window.columnconfigure(2, weight=1)
    detail_window.columnconfigure(3, weight=1)

    detail_window.rowconfigure(0, weight=1)
    detail_window.rowconfigure(1, weight=2)
    detail_window.rowconfigure(2, weight=1)
    detail_window.rowconfigure(3, weight=1)
    detail_window.rowconfigure(4, weight=1)
    detail_window.rowconfigure(5, weight=1)
    detail_window.rowconfigure(6, weight=1)
    detail_window.rowconfigure(7, weight=1)
    detail_window.rowconfigure(8, weight=1)

    # titles for two parts
    Label(detail_window, text='Detail Information', font=('Arial Bold', 20), pady=5, padx=5).grid(row=0, column=0,
                                                                                                  columnspan=2)
    Label(detail_window, text='restaurant name:', font=('Bold', 10), pady=5, padx=5).grid(row=1, column=0)
    name_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    name_label.grid(row=1, column=1)

    Label(detail_window, text='cuisines:', font=('Bold', 10), pady=5, padx=5).grid(row=2, column=0)
    cuisines_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    cuisines_label.grid(row=2, column=1)

    Label(detail_window, text='opening time:', font=('Bold', 10), pady=5, padx=5).grid(row=3, column=0)
    time_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    time_label.grid(row=3, column=1)

    Label(detail_window, text='call:', font=('Bold', 10), pady=5, padx=5).grid(row=4, column=0)
    call_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    call_label.grid(row=4, column=1)

    Label(detail_window, text='mark:', font=('Bold', 10), pady=5, padx=5).grid(row=5, column=0)
    mark_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    mark_label.grid(row=5, column=1)

    Label(detail_window, text='review number:', font=('Bold', 10), pady=5, padx=5).grid(row=6, column=0)
    review_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    review_label.grid(row=6, column=1)

    Label(detail_window, text='location detail:', font=('Bold', 10), pady=5, padx=5).grid(row=7, column=0)
    location_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    location_label.grid(row=7, column=1)

    Label(detail_window, text='location link:', font=('Bold', 10), pady=5, padx=5).grid(row=8, column=0)
    link_label = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    link_label.grid(row=8, column=1)

    # Label(detail_window, text='Bus Routes in Adelaide', font=('Arial Bold', 10), pady=5, padx=5).grid(row=0, column=2)
    res_list = Listbox(detail_window, width=50, height=20, border=0)
    res_list.grid(column=2, row=1)

    #read data from exsited csv or crawler
    #file = open(
        #r"../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/86cf176018a02243e8e2dfdfaf9513ae/Message/MessageTemp/3c7ee09f21558ddc06641c369359cfa4/File/restaurant.csv", encoding='unicode_escape')
    
    #to get data from crawler, uncomment following two line, and comment the third line
    #restaurant_crawler.create_restaurant_csv()
    #file = open(r"backupcsv/restaurant1.csv", encoding='unicode_escape')
    file = open(r"backupcsv/restaurant.csv", encoding='unicode_escape')
    reader = csv.reader(file)
    data = list(reader)

    list_of_entries = []
    for x in list(range(1, len(data))):
        list_of_entries.append(data[x][1])

    for x, y in enumerate(list_of_entries):
        res_list.insert(x, y)

    # show restaurant detail
    def show_details():
        index = res_list.curselection()[0]+1
        name_label.config(text=data[index][1])
        cuisines_label.config(text=data[index][2])
        time_label.config(text=data[index][3])
        call_label.config(text=data[index][4])
        mark_label.config(text=data[index][5])
        review_label.config(text=data[index][6])
        location_label.config(text=data[index][7])
        link_label.config(text=data[index][8])

    button2 = Button(detail_window, text="See detail info", command=show_details)
    button2.grid(row=8, column=2)


def create_supermarket_window():
    '''
    display supermarket list in Adelaide
    '''
    #create new window
    supermarket_window = Toplevel(root)
    supermarket_window.title('Supermarkets')
    #supermarket_window.resizable(0, 0)
    supermarket_window.geometry('800x600')

    # read from csv
    #source_data = pd.read_csv("supermarkets.csv")
    #lst = source_data.values.tolist()
    #lst = read_supermarkets_csv()
    
    # define columns
    columns = ('Name', 'Address', 'Phone','Website')

    tree = ttk.Treeview(supermarket_window, columns=columns, show='headings',height=31)

    # define headings
    tree.heading('Name', text='Name')
    tree.heading('Address', text='Address')
    tree.heading('Phone', text='Phone')
    tree.heading('Website', text='Website')
    
    # read from csv
    #source_data = pd.read_csv(
        #"../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/86cf176018a02243e8e2dfdfaf9513ae/Message/MessageTemp/3c7ee09f21558ddc06641c369359cfa4/File/supermarkets.csv")
    #lst = source_data.values.tolist()
    
    lst = read_supermarkets_csv()
    table = []
    table.append(["Name","Address","Phone","Website"])
    # new table
    for row in lst:
        #for column in total_columns:
        new_row = []
        new_row.append(row[0])
        new_row.append(row[1])
        new_row.append(row[4])
        new_row.append(row[5])
        table.append(new_row)
        
    contacts = table
    # add data to the treeview
    for contact in contacts:
        tree.insert('', END, values=contact)
        
    tree.grid(row=0, column=0, sticky='nsew')
    
    # add a scrollbar
    scrollbar = ttk.Scrollbar(supermarket_window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')



def create_busstop_window():
    '''
    display busstops in adelaide
    display detail information of selected item
    '''

    detail_window = Toplevel()
    detail_window.title('Bus Routes in Adelaide')
    #detail_window.resizable(0, 0)
    detail_window.geometry('800x600')

    detail_window.columnconfigure(0, weight=1)
    detail_window.columnconfigure(1, weight=1)
    detail_window.columnconfigure(2, weight=1)
    detail_window.columnconfigure(3, weight=1)

    detail_window.rowconfigure(0, weight=1)
    detail_window.rowconfigure(1, weight=2)
    detail_window.rowconfigure(2, weight=1)
    detail_window.rowconfigure(3, weight=1)


    Label(detail_window, text='Detail Information', font=('Arial Bold', 20), pady=5, padx=5).grid(row=0, column=0,
                                                                                                  columnspan=2)

    Label(detail_window, text='link:', font=('Bold', 10), pady=5, padx=5).grid(row=1, column=0)
    url_label2 = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    url_label2.grid(row=1, column=1)

    Label(detail_window, text='route name:', font=('Bold', 10), pady=5, padx=5).grid(row=2, column=0)
    route_label2 = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    route_label2.grid(row=2, column=1)

    Label(detail_window, text='description:', font=('Bold', 10), pady=5, padx=5).grid(row=3, column=0)
    description_label2 = Label(detail_window, text="", font=('Bold', 10), pady=5, padx=5, wraplength=100)
    description_label2.grid(row=3, column=1)


    # Label(detail_window, text='Bus Routes in Adelaide', font=('Arial Bold', 10), pady=5, padx=5).grid(row=0, column=2)
    bus_list = Listbox(detail_window, width=50, height=30, border=0)
    bus_list.grid(column=2, row=1)
    
    # to get data from crawler, uncomment following line:
    #bus.create_bus_csv()
    
    #insert data into busstop list
    file = open(r"backupcsv/bus_info.csv")
    reader = csv.reader(file)
    data = list(reader)

    list_of_entries = []
    for x in list(range(1, len(data))):
        list_of_entries.append(data[x][1])

    for x, y in enumerate(list_of_entries):
        bus_list.insert(x, y)

    # show bus routes detail
    def show_details():
        index = bus_list.curselection()[0]
        route_label2.config(text = data[index + 1][1])
        description_label2.config(text = data[index + 1][2])
        url_label2.config(text = data[index + 1][3])


    button1 = Button(detail_window, text="See detail info", command=show_details)
    button1.grid(row=3, column=2)



def create_main_window():
    '''
    create dash board
    provide entry for search, display restaurant, supermarket, busstop and news
    '''
    root.title('Rental Helper')
    #root.resizable(0, 0)
    root.geometry('800x600')

    #layout on the root window
    root.rowconfigure(0,weight=2)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2,weight=1)
    root.rowconfigure(3, weight=1)


    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=1)


    # title label
    Label(root, text = 'Your Rental Helper', font=('Arial Bold', 24), pady=20, padx=20).grid(row=0, column=0, columnspan=2, sticky='W') 

    #buttoms
    search_btn = Button(root, text='Search Housing', font=('Arial', 20), width=15, command=create_houselist_window)
    search_btn.grid(row=1, column=0, pady=5, padx=5)
    
    display_rs_btn = Button(root, text='Display Restaurant', font=('Arial', 20), width=15, command=create_restaurant_window)
    display_rs_btn.grid(row=1, column=1, pady=5, padx=5)
    
    display_sm_btn = Button(root, text='Display Suparmarket', font=('Arial', 20), width=15, command=create_supermarket_window)
    display_sm_btn.grid(row=2, column=0, pady=5, padx=5)
    
    display_bs_btn = Button(root, text='Display Bus-stop', font=('Arial', 20), width=15, command=create_busstop_window)
    display_bs_btn.grid(row=2, column=1, pady=5, padx=5)
    
    news_btn = Button(root, text='Rental News FYI', font=('Arial', 20), width=20, command=create_news_window)
    news_btn.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
    
    #show the page
    root.mainloop()

if __name__ == "__main__":
    create_main_window()