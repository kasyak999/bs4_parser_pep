# Проект парсинга pep
Развитие языка Python сопровождается документами PEP — Python Enhancement Proposal. 

### Задание
- спарсить данные обо всех документах PEP;
сравнить статус на странице PEP со статусом в общем списке;
- посчитать количество PEP в каждом статусе и общее количество PEP; данные о статусе документа нужно брать со страницы каждого PEP, а не из общей таблицы;
- сохранить результат в табличном виде в csv-файл.

Итоговая таблица должна состоять из двух колонок: «Статус» и «Количество». Последнюю строку таблицы назовите Total и выведите в ней общее количество PEP. 

## Установка
1. Создать виртуальное окружение.
    ```bash
    python -m venv venv
    ```
2. Установить зависимости.
    ```bash
    pip install -r requirements.txt
    ```
3. Запустить.
    ```bash
        python main.py <режим>
    ```
<br>

Что бы посмотреть доступные режимы запуска ```python main.py -h```
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
**pretty** - таблица

**file** - сохранить в файл