from bs4 import BeautifulSoup

OUTPUT_PATH = './text_files/featured/'

def parse(raw_html):
    """parse the raw_html and save the title and body text into a .txt. file"""
    soup = BeautifulSoup(raw_html, 'html.parser')
    title = soup.title.string
    body = soup.find(id = 'bodyContent').get_text()
    to_output = title + "\n\n" + body
    save_as_txt(to_output, title)
    print(title + '.txt saved')


def save_as_txt(text, title):
    """save text into a file named [title].txt"""
    if '/' in title: # remove forward slash from titles to avoid illegal file names
        title = title.replace('/', '')

    with open(OUTPUT_PATH + title + '.txt', 'w') as f:
        f.write(text)
