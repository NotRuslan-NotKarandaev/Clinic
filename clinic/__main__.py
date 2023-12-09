"""Start of program."""
from modules import io
from modules import models as m
from menus import main_and_startup


m.create_tables(
    m.Patient,m.Doctor,
    m.Appointment,m.Vocation,
    m.Shedule,m.User,
    m.Admin)

indent_contr = io.IndentationController()
result = main_and_startup.main_menu(indent_contr)

