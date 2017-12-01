import os
import parser
import threading
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def getTop5000():
    articles = pd.read_csv('top5000.tsv', delimiter='\t')
    featured = articles[pd.notnull(articles.ix[:, 3])]
    for idx, art in featured.iterrows():
        print('getting', art['Article'])
        r = requests.get("https://en.wikipedia.org" + art['href'])
        parser.parse(r.text)


def getPages(href, output_path):
    """get all pages in a category"""
    url_head = "https://en.wikipedia.org"
    cat_page = requests.get(url_head + href)
    cat_page_soup = BeautifulSoup(cat_page.text, 'html.parser')
    try:
        cat_group_div = cat_page_soup.find(id='mw-pages').find(class_="mw-content-ltr")
        a_tags = cat_group_div.find_all('a')
        for a_tag in a_tags:
            href = a_tag.get('href')
            href_r = requests.get(url_head + href)
            parser.parse(href_r.text, output_path)
    except:
        print("No pages found in", href)


def getCat(href, main_cat_name=None, currentDepth=0, maxDepth=1, parent_path='./text_files/'):
    """recursively get all pages the subcategories of a category
    if main_cat_name is passed, call itself again, but passing the href to
    the main_cat_name category page instead
    :param href reference to the category page
    :param main_cat_name the name of the main category
    :param maxDepth the depth of the subcategories to look through"""
    if currentDepth > maxDepth:
        return

    if main_cat_name is not None:
        directory_path = parent_path + main_cat_name + '/'
        if not os.path.exists(directory_path):  # create a directory if it does not already exist
            os.makedirs(directory_path)
        getCat("/wiki/Category:" + main_cat_name, parent_path=directory_path)
    else:
        print("Current href:", href, 'depth:', currentDepth)
        cat_name = href.split(':', 2)[1]
        directory_path = parent_path + cat_name + '/'
        if not os.path.exists(directory_path):  # create a directory if it does not already exist
            os.makedirs(directory_path)
        url_head = "https://en.wikipedia.org"
        r = requests.get(url_head + href)
        soup = BeautifulSoup(r.text, 'html.parser')
        subcat_div = soup.find(id='mw-subcategories')
        if subcat_div is not None:
            subcats = subcat_div.find_all('a')
            for subcat in subcats:
                # create a thread for each subcategory
                subcatThread = threading.Thread(target=getCat, args=[subcat.get('href')],
                                                kwargs={'currentDepth': currentDepth + 1,
                                                        'parent_path': directory_path})
                subcatThread.start()
            print(href, "completed.")
        getPages(href, directory_path)


startTime = time.time()
getCat("", main_cat_name='Equations')
print('time elapsed:', time.time() - startTime)
