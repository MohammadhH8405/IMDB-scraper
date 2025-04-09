import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
url  = 'https://www.imdb.com/chart/top/'
text = requests.get(url, headers=headers)
soup = BeautifulSoup(text.text, 'html.parser')
movies =[]

for i in soup.find_all('li',class_="ipc-metadata-list-summary-item") :
    title = i.find('h3', class_='ipc-title__text').get_text(strip=True)
    print(title)
