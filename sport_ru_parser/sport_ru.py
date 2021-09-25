import requests
import lxml.html
from lxml import etree

user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'
}

session = requests.Session()
session.headers.update(user_agent)

def get_titles(html_string):
  tree = lxml.html.document_fromstring(html_string)
  sports_titles = tree.xpath("//*[@class='h2']/text()")
  return sports_titles

def get_contents(html_string):
  tree = lxml.html.document_fromstring(html_string)
  sports_contents = tree.xpath("//*[@class='js-active js-material-list__blogpost material-list__item clearfix piwikTrackContent piwikContentIgnoreInteraction']/p/text()")
  return sports_contents

def get_links(html_string):
  tree = lxml.html.document_fromstring(html_string)
  sports_links = tree.xpath("//*[@class='h2']/@href")
  return sports_links

responce = session.get('https://www.sports.ru/football/')
title_sport = get_titles(responce.text)
content_sports = get_contents(responce.text)
links_sports = get_links(responce.text)
for i in content_sports:
  if i == '   ':
    content_sports.remove(i)

sport_ru = dict(enumerate(title_sport, start=1))
for i,j in sport_ru.items():
  print(f'Новость {i}\n{j}\n')

try:
  number = int(input('Выберите номер новости(1-20)\n'))
  print(links_sports[number-1])
except IndexError:
  print('Нужно ввести число от 1 до 20')
except ValueError:
  print('Нужно ввести число а не строку')
