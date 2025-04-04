import requests_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL, EXPECTED_STATUS


PEP_URL = 'https://peps.python.org/'


if __name__ == '__main__':
    session = requests_cache.CachedSession()
    # Очистка кеша.
    # session.cache.clear()
    response = session.get(PEP_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    sections = soup.find_all(
        'table', attrs={'class': 'pep-zero-table docutils align-default'})
    results = [('Статус', 'Ссылка', 'PEP')]
    status_list = dict()
    for section in tqdm(sections):
        tables = section.find_all('tr', attrs={'class': 'row-odd'})
        for table in tables:
            status = table.find('abbr')
            peps = table.find('a', attrs={'class': 'pep reference internal'})
            if peps:
                href = peps['href']
                version_link = urljoin(PEP_URL, href)
                response = session.get(version_link)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, features='lxml')
                preview_status = status.text[1:]
                status_pep = soup.find('abbr')
                if status_pep.text in EXPECTED_STATUS[preview_status]:
                    status_list[status_pep.text] = status_list.get(
                        status_pep.text, 0) + 1
                else:
                    print('не совпадает')
                # print(qwe.text, version_link)
                # print(qwe)
        # print('---------------------------------------')
    print(status_list)
    # print(status_list)
