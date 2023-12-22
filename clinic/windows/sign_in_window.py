from windows.base_window import Window
from modules.table import get_table_by_name
from menus.main_and_startup import sign_in as s_in,AccessLevel
from windows.message_boxes import get_message_box
from PyQt5.QtWidgets import QMessageBox


class SignInWindow(Window):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._ui_path = "ui/sign_in_window.ui"
        self.setup_ui()


    def setup_ui_base(self):
        self.help_text_path = "resources/help/sign_in_window.txt"


    def connect_signals_slots(self):
        self.sign_in_button.clicked.connect(self.sign_in)


    def sign_in(self):
        email = self.email_le.text()
        password = self.password_le.text()

        users = get_table_by_name("Users")
        try:
            access_lvl,_id = s_in(users,email,password)
            if access_lvl == AccessLevel.UNKNOWN:
                raise Exception(
                    "Can't find any persons related with"
                    " this user. Try to sign up with this"
                    " email and password.")
        except Exception as ex:
            self.msg = get_message_box(self,str(ex),QMessageBox.Warning)
            self.msg.show()
        else:
            self.close()
            self.parent().hide()
            _w = self.parent().get_next_window(access_lvl,email,_id)


    def closeEvent(self, event):
        self.parent().show()
        self.close()
