from modules import io,table,models,matrix
from menus.account_menu import account_menu
from menus.new_appointment_menu import new_appointment_menu
from menus.appointments_for_patient import appointments_for_patient
import common


def print_patient_menu_cmds(indent_contr):
    """Shows commands for patient."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - my account;\n'
        '4 - doctors;\n'
        '5 - my appointments;\n'
        '6 - remove account.')


@io.loop(False,6,print_patient_menu_cmds)
def patient_menu(indent_contr,code,*,_id:int):
    """Menu for patient."""
    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in statup menu.")
        case 3:
            tables = get_tables_related_to_patient_account(_id)

            result = account_menu(indent_contr,
                tables=tables,is_doctor=False)
        case 4:
            tables = common.get_doctors_info()

            result = new_appointment_menu(indent_contr,
                p_id=_id,tables=tables)
        case 5:
            tables = common.get_tables_related_to_appointments(p_id=_id)

            result = appointments_for_patient(indent_contr,
                tables=tables)
        case 6:
            appointments,*_ = \
                common.get_tables_related_to_appointments(p_id=_id)
            appointments.full_access = True
            appointments.update_cached()

            a_ids = list(map(lambda x: x.number,
                matrix.get_column(0,appointments.cached[1:])))
            d_ids = list(map(lambda x: x.number,
                matrix.get_column(7,appointments.cached[1:])))

            patients,users = get_tables_related_to_patient_account(_id)
            patients.full_access = True
            users.full_access = True

            patients.remove_entry(_id)
            users.remove_entry(users.ids[0])

            for a_id in a_ids:
                appointments.remove_entry(a_id)

            for d_id in d_ids:
                doctor_appointments,*_ = \
                    common.get_tables_related_to_appointments(d_id=d_id)
                shedules = common.get_shedule(d_id)
                common.optimize_appointments(doctor_appointments,shedules)

            raise io.BackToPreviousException(
                "You are now in statup menu.")
    return result


def get_tables_related_to_patient_account(p_id:int):
    """Returns Patients, Users tables
    with entry related to the patient."""
    patients = table.get_table_by_name("Patients",False)
    patients.ids = [p_id]
    u_id = patients.get_wrapper(p_id,"user").number

    users = table.get_table_by_name("Users",False)
    users.ids = [u_id]

    return [patients,users]

