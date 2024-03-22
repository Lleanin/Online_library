import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

for book_number in range(1, 11):
    payload = {
        "id": book_number
        }
    url = f'https://tululu.org/l55/{book_number}/'
    response = requests.get(url, params=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    books_block = soup.find_all(class_='d_book')
    books = [book.find('a')['href'] for book in books_block]
    for book in books:
        full_url = urljoin(url, book)
        print(full_url)
