from modules import io,table,models


def print_account_menu_cmds(indent_contr):
    """Shows commands for account of
    doctor or patient."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - show personal data;\n'
        '4 - change property.')


@io.loop(False,4,print_account_menu_cmds)
def account_menu(indent_contr,code,*,tables,
                 is_doctor:bool):
    "Account menu for patient or doctor."
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 2:
            if is_doctor:
                raise io.BackToPreviousException(
                    "You are now in doctor menu.")
            raise io.BackToPreviousException(
                "You are now in patient menu.")
        case 3:
            indent_contr.print_text(
                joined.as_str(),"Your account")
        case 4:
            p_name = indent_contr.get_input_parameter(
                "Property name",str)
            value = indent_contr.get_input_parameter(
                "New value",str)
            for _table in tables:
                if p_name in _table.fields_names_r:
                    _id = _table.ids[0]
                    _table.update_field(_id,p_name,
                        value)
                    break
