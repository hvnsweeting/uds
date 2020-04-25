#!/usr/bin/env python
# vim: ft=python
# TODO support py2 if requests_html supports
__doc__ = "Simple CLI for searching word meanings from UrbanDictionary"


import urllib

import requests_html


def cambridge(word):
    url = "https://dictionary.cambridge.org/dictionary/english/{}"

    sess = requests_html.HTMLSession()
    resp = sess.get(url.format(urllib.parse.quote(word)))
    ipa = resp.html.xpath('//span[@class="ipa dipa lpr-2 lpl-1"]')
    for i in ipa:
        print(i.text, end=" ")
    print()

    ms = resp.html.xpath('//div[@class="def ddef_d db"]')
    return url, [m.text for m in ms]


def urbandictionary(word):
    """
    >>> "misleading" in " ".join(urbandictionary("red herring"))
    True
    >>> "that feel when" in " ".join(urbandictionary("tfw")).lower()
    True
    """
    sess = requests_html.HTMLSession()
    url = "https://www.urbandictionary.com/define.php?term={}".format(
        urllib.parse.quote(word)
    )
    r = sess.get(url)
    meaning_divs = r.html.xpath('//div[@class="meaning"]')
    if not meaning_divs:
        if "There are no definitions for this word" in r.html.full_text:
            return []
        else:
            raise Exception(
                "Unknown result for {}: {}".format(word, r.html.text)
            )

    return url, [node.text for node in meaning_divs]


def get_meanings(word, source="urban"):
    if source == "urban":
        return urbandictionary(word)
    else:
        return cambridge(word)


def _test():
    import doctest

    doctest.testmod()