import parser
import requests
from bs4 import BeautifulSoup

r = requests.get('https://en.wikipedia.org/wiki/List_of_Grey%27s_Anatomy_episodes')
soup = BeautifulSoup(r.text, 'html.parser')
title = soup.title.string
print(title)
#parser.parse(r.text)