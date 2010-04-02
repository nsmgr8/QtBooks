from PyQt4.QtGui import QTableWidget, QTableWidgetItem
from PyQt4.QtCore import Qt, SIGNAL

import json

from conf import LIBRARY

def get_library():
    with open(LIBRARY, 'r') as f:
        try:
            library = json.load(f)
        except Exception, e:
            print(e)
            library = {'books': []}
    return library

class Library(QTableWidget):

    def __init__(self, book_view, parent=None):
        super(Library, self).__init__(parent=parent)
        self.book_view = book_view

        self.setColumnCount(2)
        self.refresh()

        self.create_connections()

    def refresh(self):
        self.library = get_library()

        self.clear()
        self.setRowCount(len(self.library['books']))

        self.setHorizontalHeaderLabels(['Title', 'Authors'])

        for i, book in enumerate(self.library['books']):
            for j, cell in enumerate((book['title'], ';'.join(book['authors']))):
                item = QTableWidgetItem(cell)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.setItem(i, j, item)

        self.resizeColumnsToContents()

    def create_connections(self):
        self.connect(self, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"),
                     self.view_book)

    def view_book(self):
        book_id = self.library['books'][self.currentRow()]['id']
        self.book_view.load_book(book_id)

