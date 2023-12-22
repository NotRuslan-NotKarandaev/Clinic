from windows.base_window import Window
from modules.table import get_table_by_name
from menus.main_and_startup import sign_in as s_in,AccessLevel
from windows.message_boxes import get_message_box
from PyQt5.QtWidgets import QMessageBox


class SignUpWindow(Window):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._ui_path = "ui/sign_up_window.ui"
        self.setup_ui()


    def setup_ui_base(self):
        self.help_text_path = "resources/help/sign_up_window.txt"


    def connect_signals_slots(self):
        self.sign_up_button.clicked.connect(self.sign_up)


    def sign_up(self):
        email = self.email_le.text()
        password = self.password_le.text()
        passport = self.passport_le.text()
        date_of_birth = self.date_of_birth_le.text()
        full_name = self.full_name_le.text()
        place_of_residence = self.place_of_residence_le.text()

        users = get_table_by_name("Users")

        patients = get_table_by_name("Patients")

        try:
            user_id = users.add_entry(f"{email},{password}")
            patient_id = patients.add_entry(
                f"{passport},{date_of_birth},{full_name},"
                f"{place_of_residence},{user_id}")
        except Exception as ex:
            self.msg = get_message_box(self,str(ex),QMessageBox.Warning)
            self.msg.show()
        else:
            self.close()
            self.parent().hide()
            _w = self.parent().get_next_window(
                AccessLevel.PATIENT,
                email,
                patient_id)


    def closeEvent(self, event):
        self.parent().show()
        self.close()
