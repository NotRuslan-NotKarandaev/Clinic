from modules import io,table,models


def print_one_table_menu_cmds(indent_contr):
    """Shows commands for work with the table
    for administrator."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - add entry;\n'
        '4 - remove entry;\n'
        '5 - edit entry;\n'
        '6 - print original table;\n'
        '7 - print cached table;\n'
        '8 - search entries by column;\n'
        '9 - sort entries by column;\n'
        '10 - filter entries by column.')


@io.loop(False,10,print_one_table_menu_cmds)
def one_table_menu(indent_contr,code,*,
                    _table,t_name):
    """Menu for work with table."""

    cols = ["ID"]
    cols.extend(_table.fields_names_r)

    match code:
        case 2:
            raise io.BackToPreviousException( \
                "You are now in admin mode menu.")
        case 3:
            str_entry = indent_contr.get_input_parameter( \
                "Entry (values separated by "
                "commas without spaces)",str)
            _table.add_entry(str_entry)
        case 4:
            _id = indent_contr.get_input_parameter( \
                "ID of entry",int)
            _table.remove_entry(_id)
        case 5:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            _id = indent_contr.get_input_parameter( \
                "Entry's ID",int)
            value = indent_contr.get_input_parameter( \
                "New value",str)
            _table.update_field(_id,c_name,value)
        case 6:
            indent_contr.print_text( \
                _table.as_str(), \
                f"Original {t_name}")
        case 7:
            indent_contr.print_text( \
                _table.as_str( \
                mode=table.Mode.CACHED), \
                f"Cached {t_name}")
        case 8:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            expr = indent_contr.get_input_parameter( \
                "Regular expression",str)

            indent_contr.print_text( \
                _table.as_str( \
                mode=table.Mode.SEARCH, \
                field_index=c_index, \
                regular_expression=expr), \
                f"Searched {t_name}")
        case 9:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            is_reverse = bool(indent_contr.get_input_parameter( \
                "Is reversed (0 or 1)",int))

            indent_contr.print_text( \
                _table.as_str( \
                mode=table.Mode.SORT, \
                field_index=c_index, \
                reverse=is_reverse), \
                f"Sorted {t_name}")
        case 10:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            start = indent_contr.get_input_parameter( \
                "Start value",str)
            end = indent_contr.get_input_parameter( \
                "End value",str)

            indent_contr.print_text( \
                _table.as_str( \
                mode=table.Mode.FILTER, \
                field_index=c_index, \
                start=start,end=end), \
                f"Filtered {t_name}")
