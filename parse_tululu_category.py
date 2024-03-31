import requests
import json
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from main import parse_book_page, download_image, download_txt


def main():
    parser = argparse.ArgumentParser(
        description='Данная программа берет книги сайта tululu.org и скачивает их(текст и картинки книг)'
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
        default=5
    )
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
            
            
            filename = f'{book_parameters["name"]}.txt'
            download_txt(req, filename)

            photo_url = urljoin(book_url, book_parameters["book_url"])
            download_image(photo_url)
    
    book_archive = json.dumps(book_archive, ensure_ascii=False).encode('utf8')
    with open("books.json", "w") as my_file:
        my_file.write(book_archive.decode())

    
if __name__ == '__main__':
    main()