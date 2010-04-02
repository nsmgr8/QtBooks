# -*- coding: utf-8 -*-

from PyQt4.QtGui import (QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout,
                         QVBoxLayout, QTableWidget, QTableWidgetItem,
                         QProgressDialog, QMessageBox)
from PyQt4.QtCore import SIGNAL, Qt

import json

from feedbooks import FeedBooks, Book
from library import get_library
from conf import LIBRARY

class Search(QDialog):

    def __init__(self, parent=None, lib_view=None):
        super(Search, self).__init__(parent=parent)
        self.lib_view = lib_view

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        label = QLabel("Your query:")
        self.query_edit = QLineEdit()
        self.find_button = QPushButton("Search")
        self.get_button = QPushButton("Get selected books")

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Select', 'Name', 'URL'])

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.query_edit)
        hbox.addWidget(self.find_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        vbox.addWidget(self.get_button)

        self.setLayout(vbox)

    def create_connections(self):
        self.connect(self.find_button, SIGNAL('clicked()'), self.render_result)
        self.connect(self.get_button, SIGNAL('clicked()'), self.download)

    def render_result(self):
        query = self.query_edit.text()
        if not query:
            return

        self.feed = FeedBooks()
        response = self.feed.search(str(query))

        if not response:
            QMessageBox.critical(self, 'Error', 'Could not get any result')
            return

        self.table.clear()
        self.table.setHorizontalHeaderLabels(['Select', 'Title', 'URL'])
        self.table.setRowCount(len(response[1]))

        for i, name in enumerate(zip(response[1], response[3])):
            item = QTableWidgetItem(1)
            item.data(Qt.CheckStateRole)
            item.setCheckState(Qt.Checked)
            self.table.setItem(i, 0, item)

            for j in range(2):
                item = QTableWidgetItem(name[j])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(i, j+1, item)

        self.table.resizeColumnsToContents()

    def download(self):
        rows = self.table.rowCount()

        progress = QProgressDialog("Downloading books...", "Abort download", 0,
                                   rows, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        to_download = [self.table.item(row, 2).text() for row in range(rows) if
                       self.table.item(row, 0).checkState() == Qt.Checked]

        for i, book in enumerate(to_download):
            progress.setValue(i)
            book_id = self.feed.download(str(book))
            if not book_id:
                QMessageBox.critical(self, 'Error', 'Could not download the '
                                     'book')
            elif book_id != -1:
                library = get_library() or {'books': []}
                book = Book(book_id)
                book.open()
                library['books'].append({'id': book.id, 'title': book.title,
                                         'authors': book.authors})
                with open(LIBRARY, 'w') as f:
                    json.dump(library, f, indent=4)

            if progress.wasCanceled():
                break

        progress.setValue(rows)
        progress.close()
        self.lib_view.refresh()


