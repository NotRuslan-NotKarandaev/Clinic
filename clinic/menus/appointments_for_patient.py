from modules import io,table,models
import common


def print_cmds_for_patient_appointments(indent_contr):
    """Shows commands for patient's appointments."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - show my appointments;\n'
        '4 - remove appointment.')


@io.loop(False,4,print_cmds_for_patient_appointments)
def appointments_for_patient(indent_contr,code,*,tables):
    "Appointments for patient."
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 2:
            raise io.BackToPreviousException( \
                "You are now in patient menu.")
        case 3:
            joined.update_cached(table.Mode.SORT,4,reverse=False)
            joined.update_cached(table.Mode.SORT,3,reverse=False)
            joined.update_cached(table.Mode.SORT,6,reverse=True)
            indent_contr.print_text(
                joined.as_str(table.Mode.CACHED),
                "Your appointments")
        case 4:
            appointments = tables[0]

            a_id = indent_contr.get_input_parameter(
                "Appointment's ID",int)

            was_over = appointments.get_wrapper(a_id,"was_over").number
            if was_over:
                raise Exception(
                    "You can't remove this. The appointment was over.")

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = common.get_shedule(d_id)

            appointments.full_access = True
            appointments.remove_entry(a_id)
            appointments.full_access = False

            doctor_appointments,*_ = \
                common.get_tables_related_to_appointments(d_id=d_id)

            common.optimize_appointments(doctor_appointments,shedules)
