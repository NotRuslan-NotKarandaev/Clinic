"""Start of program."""
import sys
from modules import io
from modules import models as m
from PyQt5.QtWidgets import QApplication
from windows.main_window import MainWindow


m.create_tables(
    m.Patient,m.Doctor,
    m.Appointment,m.Vocation,
    m.Shedule,m.User,
    m.Admin)
application = QApplication(sys.argv)
window = MainWindow()
sys.exit(application.exec_())
