# -*- coding:utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlparse
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


# 사이트에서 찾은 외부 URL을 모두 리스트로 수집
all_ext_links = set()
all_int_links = set()


def get_all_external_links(site_url):
    html = urlopen(site_url)
    domain = urlparse(site_url).scheme+"://"+urlparse(site_url).netloc
    bs_obj = BeautifulSoup(html, "html.parser")
    internal_links = get_internal_links(bs_obj, split_address(domain)[0])
    external_links = get_external_links(bs_obj, split_address(domain)[0])

    for link in external_links:
        if link not in all_ext_links:
            all_ext_links.add(link)
            print(link)
    for link in internal_links:
        if link == "/":
            link = domain
        elif link[0:2] == "//":
            link = domain + link
        elif link[0:1] == "/":
            link = domain + link

        if link not in all_int_links:
            print("about to get link: " + link)
            all_int_links.add(link)
            get_all_external_links(link)


# follow_external_only("http://oreilly.com")

domain = "http://oreilly.com"
get_all_external_links(domain)
