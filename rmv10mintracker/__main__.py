#!/usr/bin/env python3

import sys
import os
import re
from email import message_from_file
from time import strptime, strftime

from bs4 import BeautifulSoup

from .emailparser import pullout as reademail


def yield_emails():
    basedir  = os.path.dirname(sys.argv[1])
    filelist = [e for e in os.listdir(basedir) if e.lower().endswith(".eml")]

    for f in filelist:
        fullname = os.path.join(basedir, f)
        with open(fullname, "r") as emailfile:
            emailmsg = message_from_file(emailfile)
        yield emailmsg


for emailmsg in yield_emails():
    text, html = reademail(emailmsg)
    soup = BeautifulSoup(html, "lxml")

    htmltext = " ".join([
        e.strip()
        for e in soup.text.replace("\n", " ").replace("\t", " ").split(" ")
    ]).lower()

    try:
        process_number = re.search("vorgangsnummer\s([0-9]+)", htmltext)[1]
    except:
        continue

    case_approved = False

    try:
        amount = re.search("wir\serstatten(.+)euro", htmltext)[1]
        amount = re.search("von\s([0-9\\,]+)", amount)[1].replace(",", ".")
        amount = float(amount)

        deadline = re.search("bis\szum(.+)abholen", htmltext)[1]
        deadline = re.search("[0-9]{2}\\.[0-9]{2}\\.[0-9]{4}", deadline)[0]
        deadline = strptime(deadline, "%d.%m.%Y")

        case_approved = True
    except:
        pass


    if case_approved:
        print("\t".join([str(process_number), str(amount), strftime("%d.%m.%Y", deadline)]))
    else:
        #print(process_number)
        pass
