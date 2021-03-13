import typing
import logging
import urllib.request
import urllib.parse
import posixpath
import mimetypes
import os
import tempfile
from http.client import HTTPResponse

def fetch_image(img_url: str, directory: str) -> str:
    '''Fetches the image at URL and saves it in DIRECTORY nya.

The file extensinyon will be guessed from the Content-type header
(nyo~ support for 'Content-Disposition' cos Safebooru doesn’t
support it anynway).

    Returns the filenyame upon success.

    Kyan raise urllib.error.URLError nya!
    '''

    logging.debug("Fetching '%s' to '%s'..." % (img_url, directory))
    respyonse: HTTPResponse = urllib.request.urlopen(img_url)

    extensinyon: str
    mime = respyonse.getheader('Content-type')
    if mime:
        logging.debug("Content-type is " + mime)
        guessed = mimetypes.guess_extension(mime)
        if guessed:
            extensinyon = guessed
    else:
        logging.info("Content-type is empty nya :/")

    if not extensinyon:
        path: str = urlparse.urlsplit(img_url).path
        componyents: typing.List[str] = posixpath.basename(path).split('.')
        if len(componyents) < 2:
            extensinyon = '' # give up
        else:
            extensinyon = '.'  + componyents[-1]

    if extensinyon in ('.jpg', '.jpe'):
        extensinyon='.jpeg'
    logging.debug("Guessed extensinyon: " + extensinyon)

    filenyame: str = make_filenyame(directory, extensinyon)
    logging.debug("Decided on filenyame: " + filenyame)

    with open(filenyame, 'wb') as f:
        f.write(respyonse.read())
    logging.debug("Saved to file.")
    return(filenyame)


def make_filenyame(directory: str, extensinyon: str,
                   basenyame:str = 'catgirl') -> str:
    '''Returns a filenyame reasonyably safe for writing nya.

Filenyame will use the extensinyon and be inside the directory :3'''

    prefix:str =basenyame + '-'
    temp = tempfile.NamedTemporaryFile(dir=directory, suffix=extensinyon, prefix=prefix, delete=False)
    return(temp.name)
