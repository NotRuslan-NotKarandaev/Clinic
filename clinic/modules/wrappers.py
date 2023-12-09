"""Wrappers over fields."""
import re
import datetime as dt
from modules import number as n


class NotValidFormat(ValueError):
    """Throws if the format of string is not valid."""


    def __init__(self):
        super().__init__('String format is not valid.')


class CharField:
    """Char field."""
    def __init__(self, string_value):
        if not string_value is None:
            self.from_str(string_value)
        self.value = string_value


    def __str__(self) -> str:
        if self.value is None:
            return ""
        return self.value


    def __lt__(self,other):
        return str(self) < str(other)


    def __eq__(self,other):
        return str(self) == str(other)


    def __ne__(self,other):
        return not self == other


    def __le__(self,other):
        return (self < other) or (self == other)


    def __gt__(self,other):
        return not self <= other


    def __ge__(self,other):
        return (self > other) or (self == other)


    def is_in_range_inclusive(self,start,end):
        """Checks if instance is between start and end."""
        return start <= self <= end


    def from_str(self,string):
        """Assigns values from string to 
        the fields of this object.
        If input string is not valid
        throws ValueError."""
        self.value = string


class FullName(CharField):
    """Full name as a field."""


    def from_str(self,string):
        if not re.fullmatch( \
            r'\w+\s\w+(?:\s\w+)?', \
            string):
            raise NotValidFormat
        raw_full_name = string.split()
        if len(raw_full_name) == 2:
            self.name,self.surname = raw_full_name
            self.patronymic = None
        else:
            self.name,self.surname,self.patronymic = raw_full_name


class Passport(CharField):
    """Passport series and number as a field."""


    def from_str(self,string):
        if not re.fullmatch( \
            r'[\w\d]+(?:\s[\w\d]+)?', \
            string):
            raise NotValidFormat
        raw = string.split()
        if len(raw) == 2:
            self.series,self.number = raw
        else:
            self.number = raw
            self.series = None


class Date(CharField):
    """Date as a field."""


    def from_str(self,string):
        if not re.fullmatch(r'\d{1,2}\.\d{1,2}\.\d+',string):
            raise NotValidFormat
        day,month,year = map(int,string.split("."))
        self.date = dt.date(year,month,day)


    def __str__(self):
        if self.value is None:
            return ""
        return str(self.date.day) + "." + \
            str(self.date.month) + "." + \
            str(self.date.year)


    def __lt__(self, other):
        return self.date < other.date


    def __eq__(self, other):
        return self.date == other.date


class Time(CharField):
    """Time as a field."""

    MIN_SECONDS = 0
    MAX_SECONDS = 86400

    def from_str(self,string):
        if not re.fullmatch(r'\d{1,2}:\d{1,2}(?::\d{1,2})?',string):
            raise NotValidFormat
        raw = list(map(int,string.split(":")))
        if len(raw) == 3:
            hour,minute,second = raw
        else:
            hour,minute = raw
            second = 0
        self.time = dt.time(hour,minute,second)


    def __str__(self):
        if self.value is None:
            return ""
        return str(self.time.hour) + ":" + \
            str(self.time.minute) + ":" + \
            str(self.time.second)


    def __lt__(self, other):
        return self.time < other.time


    def __eq__(self, other):
        return self.time == other.time


    def to_seconds(self):
        """Returns time in seconds."""
        result = self.time.hour * 3600 + \
            self.time.minute * 60 + \
            self.time.second
        return result


    def __sub__(self,other):
        """Returns new time wrapper that being
        the substraction of 2 time wrappers converted to seconds
        and returns change of date."""
        seconds = self.to_seconds() - other.to_seconds()
        date_delta = 0
        if seconds < 0:
            seconds += self.MAX_SECONDS
            date_delta = -1
        result = self.__class__.from_seconds(seconds)
        return result,date_delta


    def __add__(self,other):
        """Returns new time wrapper that being
        the sum of 2 time wrappers converted to seconds
        and returns change of date."""
        seconds = self.to_seconds() + other.to_seconds()
        date_delta = 0
        if seconds >= self.MAX_SECONDS:
            seconds -= self.MAX_SECONDS
            date_delta = 1
        result = self.__class__.from_seconds(seconds)
        return result,date_delta


    @classmethod
    def from_seconds(cls,seconds:int):
        """Creates time wrapper from seconds."""
        if seconds < 0:
            raise n.NotPositiveException
        minutes = seconds // 60
        hours = minutes // 60
        minutes -= hours * 60
        seconds -= hours * 3600 + minutes * 60
        result = cls(f"{hours}:{minutes}:{seconds}")
        return result



class Location(CharField):
    """Location (country city street
    building apartment)"""


    def from_str(self,string):
        if not re.fullmatch(r'(?:[\w\d]+\s){4}[\w\d]+',string):
            raise NotValidFormat
        self.country,self.city, \
            self.street,self.building, \
            self.apartment = string.split()


class Email(CharField):
    """Email (local_part domain) as field."""


    def from_str(self,string):
        if not re.fullmatch(r'[\w\d]+@[\w\d]+\.[\w\d]+',string):
            raise NotValidFormat
        self.local_part,self.domain = string.split('@')


class Number(CharField):
    """Fractional number as char field."""


    def from_str(self,string):
        self.number = float(string)


    def __lt__(self, other):
        return self.number < other.number


    def __eq__(self, other):
        return self.number == other.number


class IntNumber(Number):
    """Integer number as char field."""


    def from_str(self,string):
        self.number = int(string)


class Bool(Number):
    """Bool number as char field."""


    def __str__(self):
        if self.value is None:
            return ""
        return str(self.number)


    def from_str(self,string):
        self.number = bool(int(string))
