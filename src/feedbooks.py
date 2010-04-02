#!/usr/bin/env python

import os
import urllib
import urllib2
import json
import zipfile

from BeautifulSoup import BeautifulStoneSoup

from conf import FEEDBOOKS, LIBRARY_DIR

class FeedBooks(object):

    def search(self, query):
        data = urllib.urlencode({'query': query})
        request = urllib2.Request(FEEDBOOKS + 'books/search.json', data)
        try:
            response = urllib2.urlopen(request)
            return json.load(response)
        except Exception, e:
            print("FeedBooks.search: %s" % e)
            return None

    def download(self, url, format='epub'):
        book_id = url[url.rfind('/')+1:]

        if not os.path.exists(LIBRARY_DIR):
            os.mkdir(LIBRARY_DIR)

        book_file = os.path.join(LIBRARY_DIR, book_id+'.'+format)
        if os.path.exists(book_file):
            print 'Already downloaded'
            return -1

        try:
            response = urllib2.urlopen(url+'.'+format)
            with open(book_file, 'w') as f:
                f.write(response.read())
            return book_id
        except Exception, e:
            print("FeedBooks.download: %s" % e)
            return None

class Book(object):

    _FILE = LIBRARY_DIR + '%s.epub'

    def __init__(self, id=None):
        if id:
            self.open(id)

    def open(self, id=None):
        if id:
            self.id = id

        if not self.id:
            raise Exception('Book id not set')

        self.f = zipfile.ZipFile(self._FILE % self.id, 'r')
        soup = BeautifulStoneSoup(self.f.read('META-INF/container.xml'))

        oebps = soup.findAll('rootfile')[0]['full-path']
        folder = oebps.rfind(os.sep)
        self.folder = '' if folder == -1 else oebps[:folder+1]

        soup = BeautifulStoneSoup(self.f.read(oebps))
        ncx = soup.findAll('item', {'id': 'ncx'})[0]
        ncx = self.folder + ncx['href']

        s = BeautifulStoneSoup(self.f.read(ncx))
        self.title = s.doctitle.text.contents[0]
        self.authors = [auth.contents[0] for auth in
                        s.docauthor.findAll('text')]

        self.chapters = [(nav.navlabel.text.contents[0], nav.content['src']) for
                         nav in s.findAll('navmap')[0].findAll('navpoint')]

    def get_chapter(self, num):
        return self.f.read(self.folder+self.chapters[num][1])


if __name__ == '__main__':
    fb = FeedBooks()
    for book in fb.search("Sherlock")[3]:
        fb.download(book, 'epub')

        b = Book(book[book.rfind('/')+1:])
        b.open()
        print '*' * 50

