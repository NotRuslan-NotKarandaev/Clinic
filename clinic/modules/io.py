"""Custom input and output of variables."""
from enum import Enum
from modules import number


class TextBlockType(Enum):
    """Types of text blocks."""
    DEFAULT = 0
    INFO = 1
    INPUT = 2
    ERROR = 3


class ResponseType(Enum):
    """Types of menu response."""
    EXIST = 0
    BACK = 1


class Wrapper:
    """Wrapper over object."""
    def __init__(self,obj,r_type:ResponseType) -> None:
        self.obj = obj
        self.r_type = r_type


class IndentationController:
    """System that controls indentations between text blocks."""


    def __init__(self,previous_text_block_type=TextBlockType.DEFAULT):
        self.previous_text_block_type = previous_text_block_type


    def try_add_indentation(self,text_block_type):
        """Adds indentation between text blocks if it's need."""
        if (self.previous_text_block_type in \
            [TextBlockType.INFO,TextBlockType.INPUT, \
            TextBlockType.ERROR]) and \
            (text_block_type in [TextBlockType.INFO, \
            TextBlockType.INPUT,TextBlockType.DEFAULT]):
            print()
        if text_block_type == TextBlockType.ERROR:
            if self.previous_text_block_type == TextBlockType.ERROR:
                print("----------AND----------")
            else:
                print("-----------+-----------")

        self.previous_text_block_type = text_block_type


    def try_get_command_code(self,end,start = 1):
        """Tries to get command code which was typed by user.
        If the code isn't in the specified range inclusive 
        the function throws Value Error."""
        command_code = self.get_input_parameter('Command code',int)
        number.check_if_number_is_in_range(command_code,start, \
            end,"Command code")
        return command_code


    def get_input_parameter(self,param_name, str_conversion,
                        cancel_word = 'x'):
        """Firstly the function will show name of input parameter, 
        then the user should type value of parameter,
        after this if the value is correct the function
        will return converted parameter 
        in other case the function will throw value error."""

        self.try_add_indentation(TextBlockType.INPUT)

        input_string = input(f'{param_name} = ')
        if input_string == cancel_word:
            raise StopProgramException

        parameter = str_conversion(input_string)
        return parameter


    def get_input_array(self,array_name,
                        str_conversion,
                        separator = ',',
                        cancel_word = 'x'):
        """Firstly the function will show name of the array, 
        then the user should type 
        values of the elements separated by the separator,
        after this if the values are correct the function
        will return converted elements as array
        in other case the function will throw ValueError."""

        self.try_add_indentation(TextBlockType.INPUT)

        print(f'{array_name}:')

        input_string = input()
        if input_string == cancel_word:
            raise StopProgramException

        str_elements = input_string.split(separator)

        array = [str_conversion(elem) \
            for elem in str_elements]

        return array


    def print_variable(self,variable_name,variable_value):
        """Prints name of variable and it's value."""
        self.try_add_indentation(TextBlockType.INFO)

        print(f"{variable_name} = {str(variable_value)}")


    def print_array(self,array_name,array):
        """Prints name of array and it's values."""
        self.try_add_indentation(TextBlockType.INFO)
        array_as_str = ' '.join(map(str,array))

        output_str = f'{array_name}:\n{array_as_str}'
        print(output_str)


    def print_exception(self,ex):
        """Prints exception message."""
        self.try_add_indentation(TextBlockType.ERROR)
        print(ex)


    def print_text(self,text,header=None):
        """Prints text."""
        self.try_add_indentation(TextBlockType.INFO)
        if not header is None:
            print(f"{header}:")
        print(text)


class StopProgramException(Exception):
    """The exception will be thrown when the user decides to stop typing."""

    def __init__(self):
        super().__init__('Program was stopped.')


class BackToPreviousException(Exception):
    """The exception will be thrown when the user decides to come back
    to the previous menu."""

    def __init__(self,message=None,
                 value_to_return=None):
        if message is None:
            super().__init__('You are back to the previous menu.')
        else:
            super().__init__(message)
        self.value_to_return = value_to_return


def loop(is_main=True,cmds_number=0,
         docs=None):
    """Loops a function with the ability
    to stop the loop. There is exception handling.
    You also can specify if this loop is main
    and add function that prints docs of the loop."""
    def wrap(func):
        def loop(indent_contr,code=None,**kwargs):
            if not docs is None:
                docs(indent_contr)
            while True:
                try:
                    code = indent_contr.try_get_command_code(cmds_number)
                    if code == 1 and (not docs is None):
                        docs(indent_contr)
                    result = func(indent_contr,code,**kwargs)
                    if not isinstance(result,Wrapper):
                        continue
                    match result.r_type:
                        case ResponseType.EXIST:
                            raise StopProgramException
                        case ResponseType.BACK:
                            if not docs is None:
                                docs(indent_contr)

                except StopProgramException as ex:
                    if is_main:
                        indent_contr.print_exception(ex)
                    result = Wrapper(None,ResponseType.EXIST)
                    return result
                except BackToPreviousException as ex:
                    indent_contr.print_exception(ex)
                    result = Wrapper(ex.value_to_return,
                                     ResponseType.BACK)
                    return result
                except Exception as ex:
                    indent_contr.print_exception(ex)

        return loop
    return wrap
