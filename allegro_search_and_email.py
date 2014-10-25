#!/bin/python
#
# Very simple script to track the offers on www.allegro.pl based on search pattern.
# Script uses BeautifulSoup for extracting relevant information from HTML
# After information is extracted, it prepares "message" and sends it over email
# The catch was building "the message" from several strings and this is where cStringIO was used.
#
# Copyright (c) astianseb
#
from bs4 import BeautifulSoup
import requests
import cStringIO

BASE_URL = "http://allegro.pl/listing/listing.php?order=m&string="
SEARCH_PATTERN = "V50+466"
GMAIL_USER = "<email account username>"
GMAIL_PASSWORD = "<email acocunt password>"

def send_email(email, msg):
    import smtplib

    gmail_user = GMAIL_USER
    gmail_pwd = GMAIL_PASSWORD
    FROM = GMAIL_USER
    TO = [email] #must be a list
    SUBJECT = "New Allegro offers!"
    TEXT = """Hello!
    \nThese are new Allegro offers!
    \n%s
    \nMessage sent by script""" % (msg)

    # Prepare actual message
    message = "From: %s\nTo: %s\nSubject: %s\n%s" % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail to %s' % email
    except:
        print "failed to send mail"

r = requests.get(BASE_URL+SEARCH_PATTERN)
soup = BeautifulSoup(r.text)

# This is necessary to "append" strings to construct full message
full_message = cStringIO.StringIO()

number = 0
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
        if number > 1:
            full_message.write(message)     #appends "message" to "full_message"

summary_message = "Number of offers: " + str(number-1)
full_message.write(summary_message)

print full_message.getvalue()

message_to_send = full_message.getvalue()
send_email("<send email to>", message_to_send)
