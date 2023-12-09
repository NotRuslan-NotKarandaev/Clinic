from modules import io,table,models
from menus.one_table_menu import one_table_menu
from menus.multi_table_menu import multi_table_menu


def print_admin_cmds(indent_contr):
    """Shows commands for administrator."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - select table;\n'
        '4 - select tables for join.')


@io.loop(False,4,print_admin_cmds)
def admin_menu(indent_contr,code,*,_id):
    """Start menu for administrator."""
    tables_names = "Admins, Appointments, Doctors, " + \
        "Patients, Shedules, Users, Vocations"

    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in statup menu.")
        case 3:
            indent_contr.print_text(tables_names,
                "Select name of one of the tables")
            t_name = indent_contr.get_input_parameter(
                "Selected table name",str)
            _table = table.get_table_by_name(t_name)

            result = one_table_menu(indent_contr,
                _table=_table,t_name=t_name)
        case 4:
            indent_contr.print_text(tables_names,
                "Select names of two or more tables")
            t_names = indent_contr.get_input_array(
                "Selected tables names "
                "(separated by commas without spaces)",str)
            tables = []
            for t_name in t_names:
                tables.append(table.get_table_by_name(t_name))
            joined = tables[0].join_with(*tables[1:])

            result = multi_table_menu(indent_contr,joined=joined)

    return result
