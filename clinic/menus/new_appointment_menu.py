from modules import io,table,models,wrappers
import common


def print_new_appointment_menu_cmds(indent_contr):
    """Shows commands for make an appointment."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - show all doctors;\n'
        '4 - schedule an appointment.')


@io.loop(False,4,print_new_appointment_menu_cmds)
def new_appointment_menu(indent_contr,code,*,p_id:int,tables):
    "Make appointments for patient."
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in patient menu.")
        case 3:
            indent_contr.print_text( 
                joined.as_str(table.Mode.SORT,8,reverse=False),
                "Doctors")
        case 4:
            d_id = indent_contr.get_input_parameter(
                "Doctor's ID",int)
            date = indent_contr.get_input_parameter(
                "Appointment's date",wrappers.Date)
            time = indent_contr.get_input_parameter(
                "Appointment's time",wrappers.Time)

            appointments,*_ = \
                common.get_tables_related_to_appointments(d_id=d_id)

            finished_ids = \
                common.get_ids_of_appointments(appointments,date)

            shedules = common.get_shedule(d_id)
            if common.check_time(
                time,shedules,finished_ids,
                appointments) is False:
                raise ValueError("This time is busy or unavailable.")

            finished_ids = \
                common.get_ids_of_appointments(appointments)

            max_date = wrappers.Date("1.1.1")
            for finished_id in finished_ids:
                max_date = max(
                    appointments.get_wrapper(finished_id.number,"real_date"),
                    max_date)
            if max_date > date:
                raise Exception("This date has already passed.")


            shedules.update_cached()
            days_in_week = shedules.cached[1][1].number
            weekday = date.date.weekday()

            if weekday >= days_in_week:
                raise Exception(
                    f"This doctor works only {days_in_week} days in week.")

            doctors = tables[0]
            average = doctors.get_wrapper(
                d_id,"average_appointment_time")

            real_end,_ = time + average

            appointments = table.get_table_by_name("Appointments")
            appointments.add_entry(
                f"{date.value},{time.value},{date.value}"
                f",{time.value},{real_end.value},{p_id},{d_id},0")

            common.optimize_appointments(appointments,shedules)