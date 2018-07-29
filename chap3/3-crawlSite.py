# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())


# 페이지내 발견된 내부링크 모두를 목록으로
def get_internal_links(bs_obj, include_url):
    internal_links = []
    # /로 시작되는 모든 링크 찾음
    for link in bs_obj.findAll("a", href=re.compile("^(/|.*" + include_url + ")")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in internal_links:
                internal_links.append(link.attrs["href"])
    return internal_links


# 페이지내 발견된 외부링크를 모두 목록으로
def get_external_links(bs_obj, exclude_url):
    external_links = []
    # 현재 URL을 포함하지 않으면서 https나 www로 시작하는 링크를 모두 찾음
    for link in bs_obj.findAll("a", href=re.compile("^(http|www)((?!" + exclude_url + ").)*$")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in external_links:
                external_links.append(link.attrs["href"])
    return external_links


def split_address(address):
    address_parts = address.replace("http://", "").split("/")
    return address_parts


def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs_obj = BeautifulSoup(html, "html.parser")
    external_links = get_external_links(bs_obj, split_address(starting_page)[0])
    if len(external_links) == 0:
        internal_links = get_internal_links(starting_page)
        return get_random_external_link(internal_links[random.randint(0, len(internal_links) - 1)])
    else:
        return external_links[random.randint(0, len(external_links) - 1)]


def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print("Random external link is " + external_link)
    follow_external_only(external_link)


follow_external_only("http://oreilly.com")
