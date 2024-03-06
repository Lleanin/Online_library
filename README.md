# Парсер книг с сайта tululu.org
Этот проект скачивает книги с сайта tululu.org .

## Как установить
Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Как запустить код

Для скачивания книг в папку books необходимо запустить файл `main.py`:

```
python main.py
```
Так же его можно запустить с аргументами `--start_page` и `--end_page`, где в качестве первого аргумента будет указано стартовая точка скачивания,а в качестве второго конечная:

```
python main.py --start_page 20 --end_page 30
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).