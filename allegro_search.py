#!/bin/python
#
# Very simple script to track the offers on www.allegro.pl based on search pattern
# and provide summary offer summary
#
# Copyright (c) astianseb

from bs4 import BeautifulSoup
import requests
import cStringIO

BASE_URL = "http://allegro.pl/listing/listing.php?order=m&string="
SEARCH_PATTERN = "V50+466"

r = requests.get(BASE_URL+SEARCH_PATTERN)

soup = BeautifulSoup(r.text)
number = 0

# This is necessary to "append" strings to construct full message
full_message = cStringIO.StringIO()


for i in soup.find_all("header"):
    number += 1
    for j in i.find_all('a'):
        href = j.get('href')
        utf_href = href.encode('utf-8')     #encode required for cStringIO to convert polish characters
        text = j.get_text()
        utf_text = text.encode('utf-8')     #encode required for cStringIO to convert polish characters
        message = """Numer: %s
http://www.allegro.pl%s
%s
---------
""" % (
            number-1,
            utf_href,
            utf_text)
        if number > 1:                      #condition added to scrap first BS search as it contains some rubbish
            full_message.write(message)
summary_message = "Number of offers: " + str(number-1)
full_message.write(summary_message)
print full_message.getvalue()
