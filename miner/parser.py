from bs4 import BeautifulSoup

OUTPUT_PATH = './text_files/'

def parse(raw_html):
    """parse the raw_html and save the title and body text into a .txt. file"""
    soup = BeautifulSoup(raw_html, 'html.parser')
    title = soup.find(id = 'firstHeading').string
    body = soup.find(id = 'bodyContent').get_text()
    to_output = title + "\n\n" + body
    save_as_txt(to_output, title)
    print(title + '.txt saved')


def save_as_txt(text, title):
    """save text into a file named [title].txt"""
    with open(OUTPUT_PATH + title + '.txt', 'w') as f:
        f.write(text)
