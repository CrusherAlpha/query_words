#!/usr/bin/env python3
import sys
import requests
from lxml import etree

def get_url():
    arg_len = len(sys.argv)
    if arg_len == 1:
        raise ValueError('No word to query, expect at least one word!')
    if arg_len == 2:
        word = sys.argv[1]
    else:
        word = '%20'.join(sys.argv[1:])
    url = 'https://dict.youdao.com/w/eng/{word}/'.format(word = word)
    return url


def get_html(url):
    return requests.get(url).text

def parse_html(html):
    selector = etree.HTML(html)
    word = selector.xpath('//span[@class = "keyword"]/text()')
    countries = selector.xpath('//div[@class = "baav"]/span[@class = \
            "pronounce"]/text()')
    countries = [country.strip() for country in countries if len(country.strip())]
    pronunciations = selector.xpath('//div[@class = "baav"]/span[@class = \
            "pronounce"]/span[@class = "phonetic"]/text()')
    if len(countries) == 0:
        countries = ['' for pronunciation in pronunciations]
    for index, pronunciation in enumerate(pronunciations):
        pronunciations[index] = countries[index] + pronunciations[index]
    meanings = selector.xpath('//div[@class = "trans-container"]/ul/li/text()')
    meanings = [meaning for meaning in meanings if len(meaning.strip())]
    return word, pronunciations, meanings

def display(word, pronunciations, meanings):
    print('')
    if len(word):
        print(word[0])
    else:
        print('Not exists this word!')
        return
    if len(pronunciations) == 1:
        print(pronunciations[0])
    if len(pronunciations) == 2:
        print('{english}  {america}'.format(english = pronunciations[0], america = pronunciations[1]))
    for meaning in meanings:
        print(meaning)


def work():
    url = get_url()
    html = get_html(url)
    word, pronunciations, meanings = parse_html(html)
    display(word, pronunciations, meanings)


if __name__ == '__main__':
    work()
