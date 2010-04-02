import os

FEEDBOOKS = "http://www.feedbooks.com/"

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
LIBRARY_DIR = os.path.join(PROJECT_DIR, 'books') + os.sep

if not os.path.exists(LIBRARY_DIR):
    os.mkdir(LIBRARY_DIR)

LIBRARY = os.path.join(LIBRARY_DIR, 'library.json')
if not os.path.exists(LIBRARY):
    open(LIBRARY, 'w').close()
