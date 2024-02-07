from bs4 import BeautifulSoup
import requests


def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('main').find('header').find('h1')
    print(title_tag.text)
    pic_link = soup.find('img', class_='attachment-post-image')['src']
    print(pic_link)
    text_tag = soup.find('div', class_='entry-content')
    print(text_tag.text)


if __name__ == '__main__':
    main()
