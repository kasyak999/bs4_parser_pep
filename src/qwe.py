import requests_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin


PEP_URL = 'https://peps.python.org/'

if __name__ == '__main__':
    session = requests_cache.CachedSession()
    # Очистка кеша.
    # session.cache.clear()
    response = session.get(PEP_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = soup.find_all(
        'table', attrs={'class': 'pep-zero-table docutils align-default'})

    for i in sidebar:
        # print(i.prettify())
        qwe = i.find_all('tr', attrs={'class': 'row-odd'})
        # print(qwe)
        for ii in qwe:
            qwer = ii.find('a', attrs={'class': 'pep reference internal'})
            if qwer:
                # print(qwer['href'])
                href = qwer['href']
                version_link = urljoin(PEP_URL, href)
                print(version_link, qwer.text)
        print('---------------------------------------')
