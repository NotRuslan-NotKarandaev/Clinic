from windows.base_window import Window
from modules.table import get_table_by_name
from menus.main_and_startup import sign_in as s_in,AccessLevel
from windows.message_boxes import get_message_box
from PyQt5.QtWidgets import QMessageBox,QLineEdit,QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AddEntryWindow(Window):
    def __init__(self,r_fields_names,
                 table_view,
                 parent=None):
        super().__init__(parent)
        self._ui_path = "ui/add_entry_window.ui"
        self.setWindowModality(Qt.ApplicationModal)
        self.r_fields_names = r_fields_names
        self.table_view = table_view
        self.setup_ui()


    def setup_ui_base(self):
        self.help_text_path = "resources/help/add_entry_window.txt"
        self.vl_items = []
        for name in self.r_fields_names:
            _le = QLineEdit()
            _le.setPlaceholderText(name)
            _le.setFont(QFont('Yu Gothic',12))
            self.vl_items.append(_le)
            self.fields_vl.addWidget(_le)


    def connect_signals_slots(self):
        self.add_entry_button.clicked.connect(self.add_entry)


    def add_entry(self):
        entry = []
        for _le in self.vl_items:
            entry.append(_le.text())
        str_entry = ','.join(entry)
        try:
            self.table_view.data.add_entry(str_entry)
            self.table_view.set_data()
        except Exception as ex:
            self.msg = get_message_box(
                self,
                str(ex),
                QMessageBox.Warning)
            self.msg.show()
        else:
            self.msg = get_message_box(
                self,
                "You successfully added entry.",
                QMessageBox.Information)
            self.msg.show()