from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class Window(QMainWindow):
    def __init__(self,parent=None,is_fixed_size=True):
        super().__init__(parent)
        self._help_text_path = None
        self.is_fixed_size = is_fixed_size


    def setup_ui(self):
        if self._ui_path is None:
            return
        loadUi(self._ui_path, self)
        self.connect_signals_slots()
        self.setup_ui_base()
        if self.is_fixed_size:
            self.setFixedSize(self.size())
        self.show()


    @property
    def help_text_path(self):
        return self._help_text_path


    @help_text_path.setter
    def help_text_path(self,value):
        self._help_text_path = value
        self.help_button.clicked.connect(self.__help)


    def __help(self):
        self.hide()
        with open(self.help_text_path) as _text:
            _w = HelpWindow(_text.read(),self)


    def setup_ui_base(self):
        pass


    def connect_signals_slots(self):
        pass


class HelpWindow(Window):
    """Shows some info that explains what
    you can do in some window."""


    def __init__(self,text,parent=None):
        super().__init__(parent)
        self._ui_path = "ui/help_window.ui"
        self._text = text
        self.setup_ui()


    def setup_ui_base(self):
        self.text.append(self._text)

    
    def closeEvent(self, event):
        self.parent().show()
        self.close()
