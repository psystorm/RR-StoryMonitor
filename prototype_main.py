import requests
from bs4 import BeautifulSoup
import sqlite3


conn = sqlite3.connect('story_mon.db')
courser = conn.cursor()

courser.execute('''CREATE TABLE IF NOT EXISTS Stories (
    StoryID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Site TEXT,
    EstimatedNextUpload TEXT,
    Description TEXT
)
''')

courser.execute('''
CREATE TABLE IF NOT EXISTS Chapters (
    ChapterID INTEGER PRIMARY KEY,
    StoryID INTEGER,
    Title TEXT NOT NULL,
    URL TEXT NOT NULL,
    DateUploaded TEXT,
    HasBeenRead BOOLEAN,
    FOREIGN KEY (StoryID) REFERENCES Stories (StoryID)
)
''')

conn.commit()

url = 'https://www.royalroad.com/fiction/85088/heavy-metal-a-monster-evolution-litrpg?utm_source=home'

#response = requests.get(url)

with open('source_test_fiction_home.txt', 'r') as file:
    html_content = file.read()
#html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

storyDict = {}

fid = soup.find_all('script')
for f in fid:
    if 'fictionId' in f.text:
        print(f.text[-7:-2])
        storyDict['fictionId'] = f.text[-7:-2]

title = soup.find('meta', {'name': 'twitter:title'}).get('content')
print(title)
storyDict['title'] = title

description = soup.find('meta', {'property': 'og:description'}).get('content')
storyDict['description'] = description
print(description)

title_url = soup.find('meta', {'property': 'og:url'}).get('content')
storyDict['title_url'] = title_url
print(title_url)

tbl = soup.find('table',{'id':"chapters"})
print(tbl['data-chapters'])
storyDict['currentChapters'] = tbl['data-chapters']

sql_cmd = '''INSERT INTO Stories (StoryID, Name, Site, EstimatedNextUpload, Description) 
                 VALUES (?, ?, ?, ?, ?)
                 '''

values = (storyDict['fictionId'], storyDict['title'], storyDict['title_url'], storyDict['currentChapters'], storyDict['description'])

conn.execute(sql_cmd, values)
conn.commit()

chapterDict = {}

tbl_rows = tbl.find_all('tr',{'class':"chapter-row"})
for row in tbl_rows:
    print(row.text.strip().split('\n')[0])
    chapterDict['chapter_title'] = row.text.strip().split('\n')[0]
    tds = row.find('td',{'class':"text-right"})
    print(tds['data-content'])
    chapterDict['chapter_index'] = tds['data-content']
    print(tds.find('a').get('href'))
    chapterDict['chapter_url'] = tds.find('a').get('href')
    print(tds.find('time').get('title'))
    chapterDict['chapter_date'] = tds.find('time').get('title')
    print(chapterDict)

    sql_cmd = '''INSERT INTO Chapters (StoryID, Title, URL, DateUploaded, HasBeenRead, ChapterID) 
                 VALUES (?,?,?,?,?,?)
                 '''
    values = (storyDict['fictionId'], chapterDict['chapter_title'], chapterDict['chapter_url'], chapterDict['chapter_date'], 0, chapterDict['chapter_index'])

    conn.execute(sql_cmd, values)
    conn.commit()

print(storyDict)

courser.execute('SELECT * FROM Stories')
res = courser.fetchall()
print(res)
courser.execute('SELECT * FROM Chapters')
res = courser.fetchall()
print(res)  

conn.close()



