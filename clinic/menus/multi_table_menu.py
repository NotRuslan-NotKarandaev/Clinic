from modules import io,table,models


def print_multi_table_menu_cmds(indent_contr):
    """Shows commands for work with the joined tables
    for administrator."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - back to the previous menu;\n'
        '3 - print original table;\n'
        '4 - print cached table;\n'
        '5 - search entries by column;\n'
        '6 - sort entries by column;\n'
        '7 - filter entries by column.')


@io.loop(False,7,print_multi_table_menu_cmds)
def multi_table_menu(indent_contr,code,*,joined):
    """Menu for wotk with joined tables."""
    t_name = "joined tables"
    match code:
        case 2:
            raise io.BackToPreviousException(
                "You are now in admin mode menu.")
        case 3:
            indent_contr.print_text(
                joined.as_str(),
                f"Original {t_name}")
        case 4:
            indent_contr.print_text(
                joined.as_str(
                mode=table.Mode.CACHED),
                f"Cached {t_name}")
        case 5:
            c_index = indent_contr.get_input_parameter(
                "Column index",int)

            expr = indent_contr.get_input_parameter(
                "Regular expression",str)

            indent_contr.print_text(
                joined.as_str(
                mode=table.Mode.SEARCH,
                field_index=c_index,
                regular_expression=expr),
                f"Searched {t_name}")
        case 6:
            c_index = indent_contr.get_input_parameter(
                "Column index",int)

            is_reverse = bool(indent_contr.get_input_parameter(
                "Is reversed (0 or 1)",int))

            indent_contr.print_text(
                joined.as_str(
                mode=table.Mode.SORT,
                field_index=c_index,
                reverse=is_reverse),
                f"Sorted {t_name}")
        case 7:
            c_index = indent_contr.get_input_parameter(
                "Column index",int)

            start = indent_contr.get_input_parameter(
                "Start value",str)
            end = indent_contr.get_input_parameter(
                "End value",str)

            indent_contr.print_text(
                joined.as_str(
                mode=table.Mode.FILTER,
                field_index=c_index,
                start=start,end=end),
                f"Filtered {t_name}")