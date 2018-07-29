# -*- coding:utf-8 -*-
import datetime
import json
import random
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

random.seed(datetime.datetime.now())


def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html, "html.parser")
    return bs_obj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


def get_history_ips(page_url):
    # 개정내역 페이지 url
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    page_url = page_url.replace("/wiki/", "")
    history_url = "http://en.wikipedia.org/w/index.php?title="
    history_url += page_url + "&action=history"
    print("history url is : " + history_url)

    html = urlopen(history_url)
    bs_obj = BeautifulSoup(html, "html.parser")

    # 사용자명 대신 ip 주소가 담긴, 클래스가 mw-anonuserlink 인 링크만 찾음
    ip_addresses = bs_obj.findAll("a", {"class": "mw-anonuserlink"})
    address_list = set()
    for ip_address in ip_addresses:
        address_list.add(ip_address.get_text())
    return address_list


def get_country(ip_address):
    try:
        response = urlopen("http://freegeoip.net/json/" + ip_address).read().decode("utf-8")
    except HTTPError:
        return None
    response_json = json.loads(response)
    return response_json.get("country_code")


links = get_links("/wiki/Python_(programming_language)")

while len(links) > 0:
    for link in links:
        print("-------------------------------------")
        history_ips = get_history_ips(link.attrs["href"])
        for history_ip in history_ips:
            country = get_country(history_ip)
            if country is not None:
                print(history_ip)

    new_link = links[random.randint(0, len(links) - 1)].attrs["href"]
    links = get_links(new_link)