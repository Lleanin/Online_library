import requests
import os
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
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


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('table').find('h1')
    title_tag = title_tag.text.split('::')
    name = title_tag[0].strip()
    author = title_tag[1].strip()

    comment_block = soup.find_all(class_='texts')
    comments = []
    for comment in comment_block:
        comment = comment.find(class_='black').text
        comments.append(comment)

    genre_block = soup.find_all(class_='d_book')
    genres = genre_block[1].find_all('a')
    books_genres = []
    for genre in genres:
        genre = genre.text
        books_genres.append(genre)

    book_url = soup.find(class_='bookimage').find('img')['src']

    book_parameters = {
        "name": name,
        "author": author,
        "comments": comments,
        "genres": books_genres,
        "book_url": book_url,
    }
    return book_parameters


def main():
    parser = argparse.ArgumentParser(
        description='Задает начальное и конечное id скачивания книг'
    )
    parser.add_argument(
        '--start_page',
        help="Начальное id",
        type=int,
        default=1
    )
    parser.add_argument(
        '--end_page',
        help="Конечное id",
        type=int,
        default=11
    )
    args = parser.parse_args()

    for i in range(args.start_page, args.end_page):
        payload = {
            "id": i
        }
        url = "https://tululu.org/txt.php?"

        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            url = f'https://tululu.org/b{i}/'
            respone_page = requests.get(url)
            respone_page.raise_for_status()

            book_parameters = parse_book_page(respone_page)
            filename = f'{i}. {book_parameters["name"]}.txt'
            download_txt(response, filename)

            photo_url = urljoin(url, book_parameters["book_url"])
            download_image(photo_url)

        except requests.exceptions.HTTPError:
            print("Такой страницы не сущетсвует!")


if __name__ == '__main__':
    main()
