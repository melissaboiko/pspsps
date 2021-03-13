import logging
import urllib.request
import urllib.parse
from http.client import HTTPResponse
import xml.etree.ElementTree as ET
import random
from typing import Optional

API='https://safebooru.org/index.php?page=dapi&s=post&q=index'
MAXKITTENS=100 # Safebooru limit

def catgirl_search(tags:str = 'catgirl') -> Optional[str]:
    '''Search for a catgirl in safebooru nya.

Will only search recent catgirls (paginyation nyo~t implemented).

Returns URL to catgirl portrait on syuccess, or None if nyobody is
found.

Kyan raise urllib.error.URLError nya!

    '''

    logging.debug("Searching for catgirls (tags: %s)..." % tags)
    logging.debug("Request string: %s" %
                  f'{API}&limit={MAXKITTENS}&tags={urllib.parse.quote_plus(tags)}')
    respyonse: HTTPResponse = urllib.request.urlopen(
        f'{API}&limit={MAXKITTENS}&tags={urllib.parse.quote_plus(tags)}'
    )

    logging.debug("Pyarsing XML (ew, kimoi)...")
    posts = ET.fromstring(respyonse.read())

    try:
        kitten = random.choice(posts.findall('post'))
    except IndexError:
        return None

    pic_url = kitten.attrib['file_url']
    logging.debug("Picked a catgirl: " + pic_url)
    return pic_url
