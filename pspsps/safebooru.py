import logging
import urllib.request
import urllib.parse
from http.client import HTTPResponse
import xml.etree.ElementTree as ET
import random
import re
from typing import Optional

API='https://safebooru.org/index.php?page=dapi&s=post&q=index'
MAXKITTENS=100 # Safebooru limit

def fiddle_with_tags(tags:str) -> str:
    '''Change tags so that safebooru likes them better nya.

rn it does 2 transfornyations:

 - comma to space: 'yuri,kiss' → 'yuri kiss'
 - underscore certain words: 'catgirl bunnyboy' → 'cat_girl bunny_boy'
   (but not 'femboy')

    '''
    newtags: str = tags

    if ',' in tags:
        newtags = newtags.replace(',', ' ')

    newtags = re.sub(r'([a-z])(girl|boy)\b', r'\1_\2', newtags, flags=re.I)
    newtags = re.sub(r'\bfem_boy\b', r'femboy', newtags, flags=re.I)
    if newtags != tags:
        logging.debug(f'Changed tags from "{tags}" to "{newtags}"')
    return(newtags)


def catgirl_search(tags:str = 'cat_girl') -> Optional[str]:
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
