#!/bin/python
#
# Very simple script to track the offers on www.allegro.pl based on search pattern
# and provide summary
#
from bs4 import BeautifulSoup
import requests
import cStringIO
import sqlite3

BASE_URL = "http://allegro.pl/listing/listing.php?order=m&string="
SEARCH_PATTERN = "V50+466"

r = requests.get(BASE_URL + SEARCH_PATTERN)

soup = BeautifulSoup(r.text)
number = 0


# This is necessary to "append" strings to construct full message
full_message = cStringIO.StringIO()

for article in soup.find_all("article"):
    article_id = article.get('data-id').encode('utf-8')
    print article_id
    for header in article.find_all('header'):
        for a in header.find_all('a'):
            href = a.get('href').encode('utf-8')
            print href
        text = header.get_text().encode('utf-8')
        print text
