# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 11:34:10 2021

@author: Lenovo

@description: generate word cloud for news keyword
"""
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import csv

def generate_keyword_cloud():
    file = open("backupcsv/news_output.csv", encoding='utf-8')
    reader = csv.reader(file)
    data = list(reader)
    data = np.array(data)
    keyword = data[:,4]
    text = " ".join(word for word in keyword)
    stopwords = set(STOPWORDS)
    stopwords.update(["Australia", "rental", "rent", "real estate","house","home","Australian"])
    wordcloud = WordCloud(width=200, height=200,stopwords=stopwords, background_color="white").generate(text)
    wordcloud.to_file("keyword_cloud.png")
