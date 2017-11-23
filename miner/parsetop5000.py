"""
Parse top5000pages.html and output the table to a .csv file
"""

from bs4 import BeautifulSoup

with open('top5000pages.html', 'r') as f:
    raw = f.read()

soup = BeautifulSoup(raw, 'html.parser')
table = soup.find("table", class_='wikitable sortable')
rows = table.find_all("tr")
table_list = []

for row in rows:
    temp = []
    for cell in row.children:
        if cell.string == '\n':
            continue
        if cell.string != None:
            temp.append(cell.string)
            if cell.a != None:
                temp.append(cell.a.get('href'))
        elif cell.img != None:
            temp.append(cell.img['alt'])
        else:
            temp.append('')
    table_list.append(temp)

with open('top5000.tsv', 'w') as f:
    table_list[0].insert(2, 'href') # add column header for links
    for row in table_list:
        f.write('\t'.join(row) + '\n')