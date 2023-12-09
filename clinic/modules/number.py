"""Operations with numbers."""
from modules import array


class NotPositiveException(ValueError):
    """Throws if the number is not positive."""


    def __init__(self):
        super().__init__('Number is not positive.')


def check_if_is_positive(number):
    """Checks if this number is positive.
    And if it is not throws NotPositiveException."""
    if number <= 0:
        raise NotPositiveException


def check_if_number_is_in_range(number,start,end,number_name):
    """Checks if the number is in range
    from the start to the end inclusive.
    And if it is not in range throws ValueError."""
    if not number in array.get_range_inclusive(start,end):
        raise ValueError(f'{number_name} must be in ' + \
        f'range from {start} to {end} inclusive.')
