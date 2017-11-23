import parser
import requests


r = requests.get("https://en.wikipedia.org/wiki/1966_New_York_City_smog")
parser.parse(r.text)