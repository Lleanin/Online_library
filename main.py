import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import os


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(response, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def main():
    for i in range(1, 11):
        payload = {
            "id": i
        }
        url = "https://tululu.org/txt.php?"

        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            url = f'https://tululu.org/b{i}/'
            Page = requests.get(url)
            Page.raise_for_status()

            soup = BeautifulSoup(Page.text, 'lxml')
            title_tag = soup.find('body').find('table').find('h1')
            title_tag = title_tag.text.split('::')

            name = title_tag[0].strip()
            filename = f'{i}. {name}.txt'
            download_txt(response, filename)
        except requests.exceptions.HTTPError:
            print("Такой страницы не сущетсвует!")


if __name__ == '__main__':
    main()
