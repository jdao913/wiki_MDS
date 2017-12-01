"""Get vital articles given page source"""

import os
import threading
from bs4 import BeautifulSoup
import requests
import parser

def run():
    """main function"""
    for filename in os.listdir('./vital_src/'):
        # get category name from html filename
        cat_name = os.path.splitext(os.path.basename(filename))[0]
        with open('./vital_src/' + filename, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        os.makedirs('./vital_src/' + cat_name + '/') # create a directory with the category name
        thread = threading.Thread(target=fetch_articles, args=[soup, cat_name]) # use threads to speed up scraping
        thread.start()

def fetch_articles(soup, cat_name):
    """fetch all the articles given by the links in soup"""
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if 'Level' in href:
            continue
        else:
            url_head = 'https://en.wikipedia.org'
            r = requests.get(url_head + href)
            parser.parse(r.text, './vital_src/' + cat_name + '/')

run()