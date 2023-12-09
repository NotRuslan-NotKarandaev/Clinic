from modules import io,table,models
from menus.account_menu import account_menu
from menus.appointments_for_doctor import appointments_for_doctor
import common


def print_doctor_menu_cmds(indent_contr):
    """Shows commands for doctor."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - my account;\n'
        '4 - my appointments.')


@io.loop(False,4,print_doctor_menu_cmds)
def doctor_menu(indent_contr,code,*,_id):
    """Menu for doctor."""
    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in statup menu.")
        case 3:
            tables = get_tables_related_to_doctor_account(_id)

            result = account_menu(indent_contr,
                tables=tables,is_doctor=True)
        case 4:
            tables = common.get_tables_related_to_appointments(d_id=_id)
            result = appointments_for_doctor(indent_contr,
                tables=tables)
    return result


def get_tables_related_to_doctor_account(d_id:int):
    """Returns Doctors, Users, Shedules, Vocations tables
    with entry related to the doctor."""
    doctors = table.get_table_by_name("Doctors",False)
    doctors.ids = [d_id]
    doctors.fields_names_w = \
        ["full_name","passport","average_appointment_time"]
    u_id = doctors.get_wrapper(d_id,"user").number
    v_id = doctors.get_wrapper(d_id,"vocation").number

    users = table.get_table_by_name("Users",False)
    users.fields_names_w = ["email","password"]
    users.ids = [u_id]

    shedules = common.get_shedule(d_id)

    vocations = table.get_table_by_name("Vocations",False)
    vocations.fields_names_w = []
    vocations.ids = [v_id]

    return [doctors,users,shedules,vocations]