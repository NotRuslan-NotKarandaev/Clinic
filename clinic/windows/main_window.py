from windows.base_window import Window
from windows.admin_window import AdminWindow
from windows.sign_in_window import SignInWindow
from menus.main_and_startup import AccessLevel
from windows.sign_up_window import SignUpWindow


class MainWindow(Window):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._ui_path = "ui/main_window.ui"
        self.setup_ui()


    def setup_ui_base(self):
        self.help_text_path = "resources/help/main_window.txt"


    def connect_signals_slots(self):
        self.sign_in_button.clicked.connect(self.sign_in)
        self.sign_up_button.clicked.connect(self.sign_up)


    def sign_in(self):
        self.hide()
        _w = SignInWindow(self)


    def sign_up(self):
        self.hide()
        _w = SignUpWindow(self)


    def get_next_window(self,access_lvl:AccessLevel,email,_id):
        """Returns admin, doctor or patient window."""
        match access_lvl:
            case AccessLevel.ADMIN:
                _w = AdminWindow(self,email=email,_id=_id)
            case AccessLevel.DOCTOR:
                raise NotImplementedError()
                #I don't have any free time to work out that.
                #For now, you can use the console version as alternative.
                _w = DoctorWindow(self,email=email,_id=_id)
            case AccessLevel.PATIENT:
                raise NotImplementedError()
                _w = PatientWindow(self,email=email,_id=_id)
        return _w
