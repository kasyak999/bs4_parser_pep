import re
from urllib.parse import urljoin

import logging

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from collections import defaultdict

# from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL, EXPECTED_STATUS
import constants
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session: requests_cache.CachedSession):
    """Что нового в Python"""
    whats_new_url = urljoin(constants.MAIN_DOC_URL, constants.WHATSNEW_PATH)
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(
        soup, 'section', attrs={'id': constants.WHATSNEW_SECTION_ID})
    div_with_ul = find_tag(
        main_div, 'div', attrs={'class': constants.WHATSNEW_DIV_CLASS})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': constants.WHATSNEW_LI_CLASS})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python, desc="Загрузка из кеша"):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session: requests_cache.CachedSession):
    response = get_response(session, constants.MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'menu-wrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session: requests_cache.CachedSession):
    downloads_url = urljoin(constants.MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    table_tag = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', attrs={'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = constants.BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session: requests_cache.CachedSession):
    response = get_response(session, constants.PEP_URL)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    sections = soup.find_all(
        'table', attrs={'class': constants.PEP_TABLE_CLASS})
    results = [('Статус', 'Количество')]
    status_list = defaultdict(int)
    total = 0
    status_false = []

    for section in tqdm(sections):
        tables = section.find_all(
            'tr', attrs={'class': constants.PEP_TR_CLASS})
        for table in tables:
            status = table.find('abbr')
            if not status:
                continue

            preview_status = status.text[1:]
            pep_link_tag = table.find(
                'a', attrs={'class': constants.PEP_A_CLASS})
            if not pep_link_tag:
                continue

            version_link = urljoin(constants.PEP_URL, pep_link_tag['href'])
            response = get_response(session, version_link)
            soup = BeautifulSoup(response.text, features='lxml')
            status_pep = find_tag(soup, 'abbr')

            if status_pep.text in constants.EXPECTED_STATUS.get(
                preview_status
            ):
                status_list[status_pep.text] += 1
            else:
                status_false.append((
                    version_link, status_pep.text,
                    constants.EXPECTED_STATUS.get(preview_status)))

            total += 1

    for key, value in sorted(status_list.items()):
        results.append((key, value))
    results.append(('Total', total))

    if status_false:
        mes_text = '\nНесовпадающие статусы:\n'
        for url, status, expected in status_false:
            mes_text += (
                f'{url}\nСтатус в карточке: {status}\n'
                f'Ожидаемые статусы: {expected}')
        logging.info(mes_text)

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
