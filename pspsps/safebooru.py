'''safebooru interface for catgirls nya'''
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
        logging.debug('Changed tags from "%s" to "%s"', tags, newtags)
    return newtags


def safebooru_list(tags: str,
                   limit: int=MAXKITTENS,
                   page: int=0,
                  ) -> HTTPResponse:
    '''Access safebooru's search API at a certain page number.

Pages appear to start at 0.'''

    reqwest: str = API + '&' + '&'.join([
        f'limit={limit}',
        f'tags={urllib.parse.quote_plus(tags)}',
        f'pid={page}',
    ])

    logging.debug("Request string: <%s>", reqwest)

    respyonse = urllib.request.urlopen(reqwest)
    assert isinstance(respyonse, HTTPResponse) # to reassyure mypy
    logging.debug("Respyonse status: %s", respyonse.status)
    return respyonse

def safebooru_count(posts: ET.Element) -> int:
    '''Parses a safebooru response XML and returns how man yposts were found.'''

    try:
        return int(posts.attrib['count'])
    except (KeyError, ValueError):
        logging.warning('Unexpected XML format from safebooru nya')
        return 0

def catgirl_search(tags:str = 'cat_girl') -> Optional[str]:
    '''Search for a catgirl in safebooru nya.

Will only search recent catgirls (paginyation nyo~t implemented).

Returns URL to catgirl portrait on syuccess, or None if nyobody is
found.

Kyan raise urllib.error.URLError nya!

    '''

    logging.debug("Searching for catgirls (tags: %s)...", tags)


    logging.debug("Pyarsing XML (ew, kimoi)...")
    # first round is just to see how many results we have, so we don’t fetch any
    respyonse = safebooru_list(tags, limit=0)
    posts = ET.fromstring(respyonse.read())
    nposts = safebooru_count(posts)

    logging.debug("Found %d catgirls", nposts)
    if nposts == 0:
        return None

    totyal_pages = int(nposts / MAXKITTENS)+1
    logging.debug("%d pages at %d each", totyal_pages, MAXKITTENS)

    page = random.randrange(totyal_pages)
    logging.debug("Going with page %d", page)

    respyonse = safebooru_list(tags, page=page)
    posts = ET.fromstring(respyonse.read())

    try:
        kitten = random.choice(posts.findall('post'))
    except IndexError:
        return None

    pic_url = kitten.attrib['file_url']
    logging.debug("Picked a catgirl: %s", pic_url)
    return pic_url
