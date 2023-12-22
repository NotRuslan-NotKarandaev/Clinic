from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QAction,
    QTableWidget,QTableWidgetItem,QVBoxLayout,
    QMenu,QHeaderView)
from PyQt5.QtGui import QIcon,QCursor
from PyQt5.QtCore import pyqtSlot,QAbstractTableModel,pyqtSignal
from PyQt5.QtCore import Qt
from windows.message_boxes import get_message_box
from PyQt5.QtWidgets import QMessageBox
from modules.table import Table,Mode


class TableView(QTableWidget):
    def __init__(self,data:Table,parent):
        cached = data.update_cached(Mode.CACHED)
        QTableWidget.__init__(
            self,
            len(cached) - 1,
            len(cached[0]),
            parent)
        self.data = data
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.db_change_lock = False

        cached = self.data.update_cached(Mode.CACHED)
        self.setHorizontalHeaderLabels(cached[0])

        self.cellChanged.connect(self.handle_cell_change)

        self.h_header = CustomHeader(Qt.Horizontal,self)
        self.setHorizontalHeader(self.h_header)
        self.h_header.rightClicked.connect(self.show_column_context_menu)
        self.h_header.sectionClicked.connect(self.sort_table)

        if data.full_access:
            self.v_header = CustomHeader(Qt.Vertical,self)
            self.setVerticalHeader(self.v_header)
            self.v_header.rightClicked.connect(self.show_row_context_menu)

        self.is_descending_order = True
        self.show()
 

    def show_row_context_menu(self,index):
        pos = QCursor.pos()

        menu = QMenu()

        action1 = menu.addAction("Remove entry")

        action = menu.exec_(pos)

        if action == action1:
            _id = self.get_entry_id()
            self.data.remove_entry(_id)
            self.set_data()


    def show_column_context_menu(self,index):
        pos = QCursor.pos()

        menu = QMenu()
        action1 = menu.addAction("Sort")
        action2 = menu.addAction("Filter")
        action3 = menu.addAction("Search")

        action = menu.exec_(pos)

        if action == action1:
            self.sort_table(index)
        elif action == action2:
            raise NotImplementedError
        elif action == action3:
            raise NotImplementedError
    

    def sort_table(self,index):
        self.is_descending_order = not self.is_descending_order
        self.data.update_cached(
            mode=Mode.SORT,
            field_index=index,
            reverse=self.is_descending_order)
        self.set_data()


    def handle_cell_change(self,row_index,
                          column_index):
        if self.db_change_lock:
            return
        item = self.item(row_index,column_index)
        _id = self.get_entry_id(row_index)
        name = self.get_field_name(column_index)
        try:
            self.data.update_field(_id,name,item.text())
        except Exception as ex:
            self.msg = get_message_box(self,str(ex),QMessageBox.Warning)
            self.msg.show()


    def set_data(self):
        self.db_change_lock = True
        cached = self.data.update_cached(Mode.CACHED)
        self.setRowCount(len(cached) - 1)
        self.setColumnCount(len(cached[0]))

        for m,row in enumerate(cached[1:]):
            for n,item in enumerate(row):
                newitem = QTableWidgetItem(item.value)
                if (n == 0) or (not self.data.full_access):
                    newitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.setItem(m,n,newitem)
        self.setHorizontalHeaderLabels(cached[0])

        self.db_change_lock = False


    def get_entry_id(self,row_index):
        cached = self.data.update_cached(Mode.CACHED)
        _id = cached[row_index + 1][0].number
        return _id


    def get_field_name(self,column_index):
        name = self.data.fields_names_r[column_index - 1]
        return name


class CustomHeader(QHeaderView):
    rightClicked = pyqtSignal(int)

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            logical_index = self.logicalIndexAt(event.pos())
            self.rightClicked.emit(logical_index)
