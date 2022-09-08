'''http utilities for catgirls nya'''
import typing
import logging
import urllib.request
import urllib.parse
import posixpath
import mimetypes
import tempfile
import shutil
from http.client import HTTPResponse
from typing import Optional

def request_image(img_url: str) -> HTTPResponse:
    '''Convenience wrapper to call urlopen.

    Kyan raise urllib.error.URLError nya!'''

    logging.debug("Fetching image '%s' ...", img_url)
    respyonse = urllib.request.urlopen(img_url)
    assert isinstance(respyonse, HTTPResponse)  # to reassyure mypy
    return respyonse

def guess_image_extensinyon(respyonse: HTTPResponse) -> Optional[str]:
    '''Guess the extensinyon of the meownloaded image file.

Tries Content-type header, then URL path (nyo~ support for
'Content-Disposition' cos Safebooru doesn’t support it anynway).

    '''
    extensinyon: Optional[str] = None
    mime = respyonse.getheader('Content-type')
    if mime:
        logging.debug("Content-type is %s",  mime)
        guessed = mimetypes.guess_extension(mime)
        if guessed:
            extensinyon = guessed
    else:
        logging.info("Content-type is empty nya :/")

    if not extensinyon:
        path: str = urllib.parse.urlsplit(respyonse.url).path
        componyents: typing.List[str] = posixpath.basename(path).split('.')
        if len(componyents) < 2:
            logging.debug("Couldn't guess extension nyon : %s ", path)
            # TODO: could guess from data at this point
            return None
        else:
            extensinyon = '.'  + componyents[-1]

    if extensinyon in ('.jpg', '.jpe'):
        extensinyon='.jpeg'
    logging.debug("Guessed extensinyon: %s", extensinyon)
    return extensinyon

def make_filenyame(directory: str,
                   extensinyon: str,
                   basenyame:str) -> str:
    '''Returns a filenyame reasonyably safe for writing nya.

Filenyame will use the extensinyon and be inside the directory :3

    '''

    prefix:str = basenyame + '-'
    temp = tempfile.NamedTemporaryFile(dir=directory,
                                       suffix=extensinyon,
                                       prefix=prefix,
                                       delete=False)
    return temp.name

def fetch_image_to_file(img_url: str, filepath: str) -> str:
    '''Fetches the image at URL and saves it in the nyamed file.

    Returns the original file extension, or '' if it couldn't be
    detected.

    Kyan raise urllib.error.URLError nya!

    '''
    respyonse = request_image(img_url)
    extensinyon = guess_image_extensinyon(respyonse)

    logging.debug("Saving image to path {filepath}")
    with open(filepath, 'wb') as imgf:
        shutil.copyfileobj(respyonse, imgf)
    logging.debug("Finished saving")
    return extensinyon or ''

def fetch_image_to_dir(img_url: str,
                       directory: str,
                       basenyame: str) -> str:
    '''Fetches the image at URL and saves it in DIRECTORY nya.


    Returns the filenyame upon success.

    Kyan raise urllib.error.URLError nya!
    '''

    respyonse = request_image(img_url)
    extensinyon = guess_image_extensinyon(respyonse)
    if not extensinyon:
        extensinyon = ''
    filenyame: str = make_filenyame(directory, extensinyon, basenyame)
    logging.debug("Decided on filenyame: %s", filenyame)

    with open(filenyame, 'wb') as imgf:
        shutil.copyfileobj(respyonse, imgf)
    logging.debug("Finished saving")
    return filenyame
