import requests
import pandas as pd
import parser


articles = pd.read_csv('top5000.tsv', delimiter='\t')
featured = articles[pd.notnull(articles.ix[:, 3])]
for idx, art in featured.iterrows():
    print('getting', art['Article'])
    r = requests.get("https://en.wikipedia.org" + art['href'])
    parser.parse(r.text)
