import requests
from pathlib import Path


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
            with open(filename, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.HTTPError:
            print("Такой страницы не сущетсвует!")


if __name__ == '__main__':
    main()
