from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


def get_message_box(parent,text,_type):
    msg = QMessageBox(parent)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setText(text)
    match _type:
        case QMessageBox.Information:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Information")
            msg.setWindowIcon(QIcon("resources/images/info_icon.png"))
        case QMessageBox.Warning:
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("resources/images/warning_icon.png"))
        case QMessageBox.Critical:
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setWindowIcon(QIcon("resources/images/error_icon.png"))

    return msg