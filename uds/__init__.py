#!/usr/bin/env python
# vim: ft=python
# TODO support py2 if requests_html supports
__doc__ = "Simple CLI for searching word meanings from UrbanDictionary"


import urllib

import requests_html


def cambridge_fr(word, dictionary="french-english"):
    url = "https://dictionary.cambridge.org/dictionary/{}/{}".format(
        dictionary, urllib.parse.quote(word)
    )

    sess = requests_html.HTMLSession()
    resp = sess.get(url)

    ipa_nodes = resp.html.xpath('//span[@class="ipa dipa"]')
    ipa = []
    for i in ipa_nodes:
        ipa.append(i.text)
    ms = resp.html.xpath('//span[@class="trans dtrans"]')
    return {"url": url, "ipa": set(ipa), "means": {m.text for m in ms}}


def cambridge(word, dictionary="english"):

    url = "https://dictionary.cambridge.org/dictionary/{}/{}".format(
        dictionary, urllib.parse.quote(word)
    )

    sess = requests_html.HTMLSession()
    resp = sess.get(url)

    ipa_nodes = resp.html.xpath('//span[@class="ipa dipa lpr-2 lpl-1"]')
    ipa = []
    for i in ipa_nodes:
        ipa.append(i.text)

    ms = resp.html.xpath('//div[@class="def ddef_d db"]')
    return {"url": url, "ipa": set(ipa), "means": {m.text for m in ms}}


def urbandictionary(word):
    """
    >>> "misleading" in " ".join(urbandictionary("red herring")["means"])
    True
    >>> "that feel when" in " ".join(urbandictionary("tfw")["means"]).lower()
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
            return url, ["There are no definitions for this word"]
        else:
            raise Exception("Unknown result for {}: {}".format(word, r.html.text))

    return {
        "url": url,
        "ipa": "",
        "means": [node.text for node in meaning_divs],
    }


def get_meanings(word, source="urban"):
    if source == "urban":
        return urbandictionary(word)
    elif source == "fr":
        return cambridge_fr(word)
    else:
        return cambridge(word)


def _test():
    import doctest

    doctest.testmod()
