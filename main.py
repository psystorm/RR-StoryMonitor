import requests
from bs4 import BeautifulSoup

url = 'https://www.royalroad.com/fiction/85088/heavy-metal-a-monster-evolution-litrpg?utm_source=home'

response = requests.get(url)

html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

tbl = soup.find('table',{'id':"chapters"})
print(tbl['data-chapters'])

tbl_rows = tbl.find_all('tr',{'class':"chapter-row"})
for row in tbl_rows:
    tds = row.find('td',{'class':"text-right"})
    print(tds['data-content'])
    print(tds.find('a').get('href'))
