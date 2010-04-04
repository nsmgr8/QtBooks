from PyQt4.QtGui import (QMainWindow, QDockWidget, QAction, QApplication,
                         QMessageBox)
from PyQt4.QtCore import Qt, SIGNAL, SLOT

from search import Search
from library import Library
from bookview import BookView

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.create_layout()
        self.create_actions()
        self.create_menus()
        self.create_connections()

    def create_layout(self):
        self.book = BookView(self)
        self.setCentralWidget(self.book)

        self.create_library_dock()

    def create_library_dock(self):
        if getattr(self, 'dock', None):
            self.dock.show()
            return

        self.dock = QDockWidget("Library", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea |
                                  Qt.RightDockWidgetArea)

        self.library = Library(self.book)
        self.dock.setWidget(self.library)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        file_menu.addAction(self.library_action)
        file_menu.addAction(self.search_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

    def create_actions(self):
        self.library_action = QAction("&Library", self)
        self.search_action = QAction("&Search", self)
        self.quit_action = QAction("&Quit", self)

        self.help_action = QAction("QtBooks Help", self)
        self.about_action = QAction("&About", self)

    def create_connections(self):
        self.connect(self.library_action, SIGNAL("triggered()"),
                     self.create_library_dock)
        self.connect(self.search_action, SIGNAL("triggered()"), self.search)
        self.connect(self.quit_action, SIGNAL("triggered()"),
                     QApplication.instance(), SLOT("closeAllWindows()"))

        self.connect(self.help_action, SIGNAL("triggered()"), self.help)
        self.connect(self.about_action, SIGNAL("triggered()"), self.about)

    def about(self):
        QMessageBox.about(self, "QtBooks", "An ebook reader")


    def help(self):
        QMessageBox.information(self, 'Help', 'Nothing yet!')

    def search(self):
        search = Search(self)
        search.show()


