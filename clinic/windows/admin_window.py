from windows.base_window import Window
from windows.sign_in_window import SignInWindow
from menus.main_and_startup import AccessLevel
from windows.sign_up_window import SignUpWindow
from windows.add_entry_window import AddEntryWindow
from PyQt5.QtWidgets import QCheckBox,QSizePolicy
from PyQt5.QtGui import QFont
from modules.table import get_table_by_name,ImpossibleToJoinTables,Mode
from windows.message_boxes import get_message_box
from widgets.table import TableView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QRect,Qt
from modules.array import get_formatted_words


class AdminWindow(Window):
    def __init__(self,parent=None,email=None,_id=None):
        super().__init__(parent)
        self.showMaximized()
        self._ui_path = "ui/admin_window.ui"
        self.email = email
        self._id = _id
        tables_names = ("Admins","Appointments","Doctors",
                        "Patients","Shedules","Users","Vocations")
        self.tables = \
            {t_name: get_table_by_name(t_name) \
            for t_name in tables_names}

        self.selected_tables_names = []
        self.table_widget = None
        self.setup_ui()


    def setup_ui_base(self):
        self.help_text_path = "resources/help/admin_window.txt"

        self.where_am_i_tb.setText('<p align="right">You are sign'
                                ' in as administrator with '
                                f'"{self.email}" email.&nbsp;</p>')

        lw = self.tables_names_vbl
        for t_name in self.tables:
            item = QCheckBox(t_name)
            item.setFont(QFont('Yu Gothic',12))

            item.stateChanged.connect(
                lambda state,t_name=t_name:
                self.state_changed(
                    state,
                    t_name))

            lw.addWidget(item)
            

    def state_changed(self,state,t_name):
        """Invokes when check box was clicked."""
        if state == 0:
            self.selected_tables_names.remove(t_name)
        else:
            self.selected_tables_names.append(t_name)


    def update_displayed_table(self):
        """Invokes after push select button."""
        if not self.table_widget is None:
            self.table_widget.setParent(None)

        if len(self.selected_tables_names) > 1:
            try:
                first_name = self.selected_tables_names[0]
                other_names = self.selected_tables_names[1:]
                data = self.tables[first_name].join_with(
                    *[self.tables[n] for n in other_names])
            except ImpossibleToJoinTables as ex:
                self.msg = get_message_box(self,str(ex),QMessageBox.Warning)
                self.msg.show()
                return
        elif len(self.selected_tables_names) == 1:
           first_name = self.selected_tables_names[0]
           data = self.tables[first_name]
        else:
            return

        self.table_widget = TableView(data,self.table_frame)
        self.table_widget.setFixedSize(self.table_frame.size())


    def connect_signals_slots(self):
        self.select_button.clicked.connect(
            self.update_displayed_table)
        self.add_entry_button.clicked.connect(
            self.add_entry)
        self.original_button.clicked.connect(
            self.show_original)


    def add_entry(self):
        if self.table_widget is None \
            or self.table_widget.parent() is None \
            or not self.table_widget.data.full_access:
            self.msg = get_message_box(
                self,
                "Can't add entry.",
                QMessageBox.Warning)
            self.msg.show()
            return

        _ew = AddEntryWindow(
            get_formatted_words(
                self.table_widget.data.fields_names_r),
            self.table_widget,
            self)


    def show_original(self):
        if self.table_widget is None \
            or self.table_widget.parent() is None:
            return
        self.table_widget.data.update_cached(Mode.ORIGINAL)
        self.table_widget.set_data()


    def closeEvent(self, event):
        self.parent().show()
        self.close()