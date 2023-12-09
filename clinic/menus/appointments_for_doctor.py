from modules import io,table,models,wrappers
import common


def print_cmds_for_doctor_appointments(indent_contr):
    """Shows commands for doctor's appointments."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - show appointments;\n'
        '4 - set end time for the first unmarked appointment;\n'
        '5 - remove the first unmarked appointment.')


@io.loop(False,5,print_cmds_for_doctor_appointments)
def appointments_for_doctor(indent_contr,code,*,tables):
    "Appointments for doctor."
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in doctor menu.")
        case 3:
            joined.update_cached(table.Mode.SORT,4,reverse=False)
            joined.update_cached(table.Mode.SORT,3,reverse=False)
            joined.update_cached(table.Mode.SORT,6,reverse=True)
            indent_contr.print_text(
                joined.as_str(table.Mode.CACHED),
                "Your appointments")
        case 4:
            appointments = tables[0]

            a_id = common.get_first_unmarked_appointment(
                appointments)

            end = indent_contr.get_input_parameter(
                "End time",wrappers.Time)

            _st = appointments.get_wrapper(a_id,"real_start")

            if _st >= end:
                raise ValueError("End time before start time.")

            appointments.update_field(a_id,"real_end",end.value)
            appointments.update_field(a_id,"was_over","1")

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = common.get_shedule(d_id)

            common.optimize_appointments(appointments,shedules)
        case 5:
            appointments = tables[0]

            a_id = common.get_first_unmarked_appointment(
                appointments)

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = common.get_shedule(d_id)

            appointments.full_access = True
            appointments.remove_entry(a_id)
            appointments.full_access = False

            common.optimize_appointments(appointments,shedules)
