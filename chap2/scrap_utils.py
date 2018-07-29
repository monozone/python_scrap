# -*- coding:utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None

    try:
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        l_title = bs_obj.body.h1
    except AttributeError as e:
        return None
    return l_title


def get_text_all(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None

    try:
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        name_list = bs_obj.findAll("span", {"class": "green"})
        for name in name_list:
            print(name.get_text())

    except AttributeError as e:
        return None



title = get_title("http://www.pythonscraping.com/pages/page1.html")
if title is None:
    print("Title could not be found")
else:
    print(title)

text_list = get_text_all("http://www.pythonscraping.com/pages/warandpeace.html")