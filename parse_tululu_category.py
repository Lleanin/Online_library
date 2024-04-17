import requests
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from parse_buisnes_books import parse_book_page, download_image, download_txt


def main():
    parser = argparse.ArgumentParser(
        description='Данная программа берет книги сайта tululu.org и скачивает их(текст и картинки книг)'
    )
    parser.add_argument('--start_page', help="Начальное id", type=int, default=1)
    parser.add_argument('--end_page', help="Конечное id", type=int, default=5)
    parser.add_argument('--skip_imgs', help="Скрипт не скачивает картинки", action='store_true')
    parser.add_argument('--skip_txt', help="Скрипт не скачивает книги", action='store_true')
    parser.add_argument('--dest_folder', help="Указывает папку в которую будут скачиваться картинки,книги и их параметры", default='Result')
    args = parser.parse_args()

    book_archive = []
    for page_number in range(args.start_page, args.end_page):
        payload = {
            "id": page_number
        }

        page_url = f'https://tululu.org/l55/{page_number}/'

        request = requests.get(page_url, params=payload)
        request.raise_for_status()

        soup = BeautifulSoup(request.text, 'lxml')
        books_block = soup.select(".d_book")
        books_ids = [book.select_one('a')['href'] for book in books_block]

        for book_id in books_ids:
            
            full_url = urljoin(page_url, book_id)
            
            page_response = requests.get(full_url)
            page_response.raise_for_status()
            book_parameters = parse_book_page(page_response)
            filename = f'{book_parameters["name"]}.txt'
            
            book_url = book_parameters["book_url"].split("/")
            book_url = f'images/{book_url[2]}'

            photo_url = urljoin(page_url, book_parameters["book_url"])
            book_archive.append({
                "name": book_parameters["name"],
                "author": book_parameters["author"],
                "img_src": book_url,
                "book_path": f"books/{filename}",
                "comments": book_parameters["comments"],
                "genres": book_parameters["genres"]
            })
                
            if not args.skip_txt:
                download_txt(request, filename, args.dest_folder)

            if not args.skip_imgs:
                download_image(photo_url, args.dest_folder)

    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    file_path = f"{args.dest_folder}/books.json"
    with open(file_path, "w", encoding='utf8') as json_file:
        json.dump(book_archive, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
