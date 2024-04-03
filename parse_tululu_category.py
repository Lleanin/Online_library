import requests
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from main import parse_book_page, download_image, download_txt


def main():
    parser = argparse.ArgumentParser(
        description='Данная программа берет книги сайта tululu.org и скачивает их(текст и картинки книг)'
    )
    parser.add_argument('--start_page', help="Начальное id", type=int, default=1)
    parser.add_argument('--end_page', help="Конечное id", type=int, default=5)
    parser.add_argument('--skip_imgs', help="Скрипт не скачивает картинки", action='store_false', default=True)
    parser.add_argument('--skip_txt', help="Скрипт не скачивает книги", action='store_false', default=True)
    parser.add_argument('--dest_folder',help="Указывает папку в которую будут скачиваться картинки,книги и их параметры", default='Result')
    args = parser.parse_args()
    
    
    url_template = 'https://tululu.org/l55/'
    book_archive = []
    for page_number in range(args.start_page, args.end_page):
        payload = {
            "id": page_number
            }
        
        book_url = f'https://tululu.org/l55/{page_number}/'
        
        req = requests.get(book_url, params=payload)
        req.raise_for_status()
        
        soup = BeautifulSoup(req.text, 'lxml')
        books_block = soup.select(".d_book")
        books_nums = [book.select_one('a')['href'] for book in books_block]
        
        for num in books_nums:
            full_url = urljoin(url_template, num)
            
            page_response = requests.get(full_url)
            page_response.raise_for_status()
            book_parameters = parse_book_page(page_response)
            book_archive.append(book_parameters)
            
            if args.skip_txt:
                filename = f'{book_parameters["name"]}.txt'
                download_txt(req, filename, args.dest_folder)

            if args.skip_imgs:
                photo_url = urljoin(book_url, book_parameters["book_url"])
                download_image(photo_url, args.dest_folder)
    
    book_archive = json.dumps(book_archive, ensure_ascii=False).encode('utf8')
    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    folder = f"{args.dest_folder}/books.json"
    with open(folder, "w") as my_file:
        my_file.write(book_archive.decode())
        
        
if __name__ == '__main__':
    main()