import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import os
from urllib.parse import urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(response, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(url, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    url = urlparse(url)
    fname = url.path.split("/")[-1]
    filepath = os.path.join(folder, fname)

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

            photo_book = soup.find(class_='bookimage').find('img')['src']
            photo_url = urljoin(url, photo_book)
            download_image(photo_url)

            comment_block = soup.find_all(class_='texts')
            comments = []
            for comment in comment_block:
                comment = comment.find(class_='black').text
                comments.append(comment)
            print(comments)

        except requests.exceptions.HTTPError:
            print("Такой страницы не сущетсвует!")


if __name__ == '__main__':
    main()
