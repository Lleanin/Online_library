import requests
from pathlib import Path
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    for i in range(1, 11):
        payload = {
            "id": i
        }
        url = "https://tululu.org/txt.php?"

        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            filename = f'books/{i}.txt'
            # with open(filename, 'wb') as file:
            #     file.write(response.content)
            url = 'https://tululu.org/b1/'
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.find('body').find('table').find('h1')
            title_tag = title_tag.text.split('::')
            print("Заголовок:", title_tag[0])
            print("Автор:", title_tag[1].strip())
        except requests.exceptions.HTTPError:
            print("Такой страницы не сущетсвует!")


if __name__ == '__main__':
    main()
