# RR-StoryMonitor
RR Story Monitor and Notifier

Using python and a database, keep track of stories I am interseted in, and notify me when they are updated.

BeautifulSoup to request url and parse page
need base url for urls scraped from pages - www.royalroad.com
can get total chapters from table of contents table - data-chapters
    tbl = soup.find('table',{'id':"chapters"})
        print(tbl['data-chapters'])

    tbl_rows = tbl.find_all('tr',{'class':"chapter-row"})
        for row in tbl_rows:
            tds = row.find('td',{'class':"text-right"})
                print(tds['data-content'])
                print(tds.find('a').get('href'))

get the ficition Id from the html
    fid = soup.find_all('script')
    for f in fid:
        if 'fictionId' in f.text:
            print(f.text[-7:-2])


cursor.execute('''
CREATE TABLE IF NOT EXISTS Stories (
    StoryID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Site TEXT,
    EstimatedNextUpload TEXT,
    Description TEXT
)
''')

# Create a table for Chapters
cursor.execute('''
CREATE TABLE IF NOT EXISTS Chapters (
    ChapterID INTEGER PRIMARY KEY,
    StoryID INTEGER,
    Title TEXT NOT NULL,
    URL TEXT NOT NULL,
    DateUploaded TEXT,
    HasBeenRead BOOLEAN,
    FOREIGN KEY (StoryID) REFERENCES Stories (StoryID)