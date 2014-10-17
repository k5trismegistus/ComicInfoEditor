import urllib.request
import urllib.parse
import bs4
import re


def search_by_url(url):
    """Get single book's metadata from Lexicon's url"""
    def get_result(soup):

        metadata = {}

        metadata['Series'] = get_series(soup)
        metadata['Writer'] = get_writer(soup)
        metadata['Penciller'] = get_penciller(soup)
        metadata['Genre'] = get_genre(soup)

        date = get_date(soup)

        metadata['Year'] = date[0]
        metadata['Month'] = date[1]
        metadata['Day'] = date[2]

        return metadata

    def get_series(soup):
        raw_series = soup.find('td', text='原題:').next_sibling
        series = raw_series.string
        return series

    def get_writer(soup):
        writer = []
        raw_writer = soup.find_all(href=re.compile('/browse/circle/[0123456789]+/'))
        for w in raw_writer:
            writer.append(w.string)
        return writer[0::2]

    def get_penciller(soup):
        penciller = []
        raw_penciller = soup.find_all(href=re.compile('/browse/author/[0123456789]+/'))
        for p in raw_penciller:
            penciller.append(p.string)
        return penciller[0::2]

    def get_genre(soup):
        genre = []
        raw_genre = soup.find_all(href=re.compile('/browse/parody/[0123456789]+/'))
        for g in raw_genre:
            genre.append(g.string)
        return genre[0::2]

    def get_date(soup):
        '''return release date in list ['year', 'month', 'day']'''
        raw_date = soup.find('td', text='発行日:').next_sibling
        raw_date = raw_date.string
        date = raw_date.split('-')

        return date

    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = bs4.BeautifulSoup(html)
    metadata = get_result(soup)

    return metadata


def search_from_keyword(keyword):
    """Search by keyword(Title) and return proposals"""

    def get_metadata(div):
        metadata = {}

        metadata['Series'] = get_series(div)
        metadata['Writer'] = get_writer(div)
        metadata['Penciller'] = get_penciller(div)
        metadata['Genre'] = get_genre(div)

        date = get_date(div)

        metadata['Year'] = date[0]
        metadata['Month'] = date[1]
        metadata['Day'] = date[2]

        return metadata

    def get_series(div):
        raw_series = div.find('span', text='原題:').next_sibling.next_sibling
        series = raw_series.string
        return series

    def get_writer(div):
        raw_writer = div.find('span', text='サークル:').next_sibling.next_sibling
        writer = raw_writer.string.string.split(',')
        return writer

    def get_penciller(div):
        raw_penciller = div.find('span', text='著者:').next_sibling.next_sibling
        penciller = raw_penciller.string.split(',')
        return penciller

    def get_genre(div):
        raw_genre = div.find('span', text='原作:').next_sibling.next_sibling
        genre = raw_genre.string.split(',')
        return genre

    def get_date(div):
        raw_date = div.find('b', text='発行日:').parent
        raw_date.b.extract()
        date = raw_date.string.split('-')
        return date

    keyword = urllib.parse.quote(keyword)
    url = 'http://www.doujinshi.org/search/simple/?T=objects&sn=' + keyword

    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = bs4.BeautifulSoup(html)

    div_bookinfos = soup.find_all('div', class_='bookinfo')

    metadatas = []
    for d in div_bookinfos:
        m = get_metadata(d)
        metadatas.append(m)

    return metadatas


if __name__ == '__main__':
    #search_by_url('http://www.doujinshi.org/book/701854/')
    for i in search_from_keyword('東方浮世絵巻'):
        print(i)