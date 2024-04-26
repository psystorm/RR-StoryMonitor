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