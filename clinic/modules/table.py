"""Wrapper over table of DB."""
import copy as co
from enum import Enum
from types import NoneType
from modules import array
from modules import matrix
from modules import models
from modules import wrappers as w


class NoAccessError(Exception):
    """Throws it if code tries to
    get refer to objects, methods, etc.
    to which it does not have access."""


    def __init__(self):
        super().__init__('Can not get access to this element.')


class ImpossibleToJoinTables(Exception):
    """Throws this if it's impossible
    to join tables."""


    def __init__(self):
        super().__init__('Can not join tables.')


class Mode(Enum):
    """Options for representation
    of table."""
    ORIGINAL = 0
    CACHED = 1
    SORT = 2
    SEARCH = 3
    FILTER = 4


class Table:
    """Wrapper of the model of table."""
    def __init__(self,entries_ids,model_class,
                 fields_names_r,fields_names_w,
                 is_full_access_to_fields=False,
                 original = None):
        self.__ids = entries_ids
        self.m_type = model_class
        self.fields_names_r = fields_names_r
        self.fields_names_w = fields_names_w
        self.full_access = is_full_access_to_fields
        self.__cached = original
        self.__original = original

    @property
    def original(self):
        """Holds matrix representation of source table."""
        return self.__original


    @original.setter
    def original(self,value):
        self.__original = value
        self.__cached = value


    @property
    def ids(self):
        """Holds ids of entries.."""
        return self.__ids


    @ids.setter
    def ids(self,value):
        self.__ids = value
        self.original = None


    @property
    def cached(self):
        """Holds matrix representation of
        sorted, searched, filtered table."""
        return self.__cached


    @cached.setter
    def cached(self,value):
        self.__cached = value


    def check_full_access(self):
        """Checks if code has full access to fields
        of this table. If it fails throws NoAccessError."""
        if not self.full_access:
            raise NoAccessError


    def add_entry(self,string,sep=","):
        """Adds and saves to db entry from string of
        separated values. Returns entry's id."""
        self.check_full_access()

        values = string.split(sep)
        names_values = self.match_to_fields(values,
                                            self.fields_names_w)
        self.m_type.check_values_for_fields(names_values)
        entry = self.m_type(**names_values)
        entry.save()
        self.ids.append(entry.id)
        self.original = None
        return entry.id


    def remove_entry(self,_id:int):
        """Removes entry from db."""
        self.check_full_access()

        entry = self.get_entry(_id)
        entry.delete_instance()
        self.ids.remove(_id)

        self.original = None


    def match_to_fields(self,vals,names):
        """Returns dictionary where to each
        field name is matched value in vals."""
        names_values = dict.fromkeys(names)
        for index,name in enumerate(names_values):
            names_values[name] = None if vals[index] == "" \
                else vals[index]
        return names_values


    def get_entry(self,_id):
        """Returns instance of model of table."""
        if not _id in self.ids:
            raise NoAccessError
        entry = self.m_type.get(id=_id)
        return entry


    def get_wrapper(self,_id:int,field_name:str):
        """Returns wrapper of field of entry 
        by entry's id and field's name."""
        field = self.get_field(_id,field_name)

        names_values = self.match_to_fields([field],[field_name])
        wrapper = self.m_type.check_values_for_fields(names_values)[0]
        return wrapper


    def get_field(self,_id:int,field_name:str)->str|None:
        """Returns value of field as string of entry 
        by entry's id and field's name."""
        if not field_name in self.fields_names_r:
            raise NoAccessError
        entry = self.get_entry(_id=_id)
        if hasattr(entry,f"{field_name}_id"):
            field = getattr(entry,f"{field_name}_id")
        else:
            field = getattr(entry,field_name)
        if field is None:
            return None
        return str(field)


    def update_field(self,_id:int,field_name:str,
                     value:str):
        """Returns value of field as string of entry 
        by entry's id and field's name."""
        if not field_name in self.fields_names_w:
            raise NoAccessError
        entry = self.get_entry(_id=_id)
        names_values = self.match_to_fields(
            [value],[field_name])
        self.m_type.check_values_for_fields(names_values)
        value = None if value == "" else value
        setattr(entry,field_name,value)
        entry.save()

        self.original = None


    def as_str(self,mode=Mode.ORIGINAL,
               field_index=None,
               regular_expression=None,
               start:str=None, end:str=None,
               reverse = None):
        """Converts table to text."""
        _matrix = self.update_cached(mode,field_index,
            regular_expression,start,end,reverse)
        return matrix.get_matrix_as_text(_matrix)


    def update_cached(self,mode=Mode.ORIGINAL,
               field_index=None,
               regular_expression=None,
               start:str=None, end:str=None,
               reverse = None):
        """Updates cached matrix with specified
        parameters. Returns new cached matrix."""
        if self.original is None:
            _matrix = self.get_matrix(
                True,of_fields=False)
        else:
            _matrix = self.cached
        match mode:
            case Mode.ORIGINAL:
                _matrix = self.get_matrix(
                    True,of_fields=False)
            case Mode.SORT:
                _matrix = matrix.get_sorted_matrix(
                    _matrix,field_index,reverse)
            case Mode.SEARCH:
                _matrix = matrix.search_in_matrix(
                    _matrix,field_index,regular_expression)
            case Mode.FILTER:
                col_type = _matrix[-1][field_index].__class__
                start = col_type(start)
                end = col_type(end)
                _matrix = matrix.filter_matrix(
                    _matrix,field_index,start,end)
        self.cached = _matrix
        return _matrix


    def get_matrix(self,with_ids = True,
                   of_fields = True):
        """Returns matrix that corresponds table
        with or without IDs of entries."""
        if with_ids:
            _matrix = self.get_matrix_with_ids(of_fields)
        else:
            _matrix = self.get_matrix_base(of_fields)
        return _matrix


    def get_matrix_with_ids(self,of_fields = True,
                            ids_column_name = "ID"):
        """Returns matrix that corresponds table
        with IDs of entries."""
        if not self.original is None:
            return self.original
        _matrix = self.get_matrix_base(of_fields)
        _matrix[0].insert(0,ids_column_name)
        for row,_id in zip(_matrix[1:],self.ids):
            row.insert(0,w.IntNumber(str(_id)))

        self.original = _matrix

        return _matrix


    def get_matrix_base(self,of_fields = True):
        """Returns matrix that corresponds table."""
        if not self.original is None:
            return self.original
        _matrix = [[] for _id in self.ids]
        for _i,_id in enumerate(self.ids):
            for name in self.fields_names_r:
                if of_fields:
                    _matrix[_i].append(self.get_field(_id,name))
                else:
                    _matrix[_i].append(self.get_wrapper(_id,name))
        names = array.get_formatted_words(self.fields_names_r)
        _matrix.insert(0,names)

        self.original = _matrix

        return _matrix


    def add_fields_names(self,names,mode="r"):
        """Adds only those names which
        there are not in already
        existed names."""
        self.cached = None
        for name in names:
            if not name in self.fields_names_r:
                self.fields_names_r.append(name)
                if mode == "w":
                    self.fields_names_w.append(name)


    def del_fields_names(self,names,mode="r"):
        """Removes only those names which
        there are in existed names."""
        self.cached = None
        for name in names:
            if name in self.fields_names_r:
                self.fields_names_r.remove(name)
                if mode == "w":
                    self.fields_names_w.remove(name)


    def join_with(self,*others):
        """Joins tables by their key fields."""
        connections,m_types = self.get_all_connections(others)
        tables = [co.deepcopy(other) for other in others]
        tables.insert(0,co.deepcopy(self))
        matrices = get_matrices_with_foreigns_keys(
            connections,m_types,tables)
        names_matrix = [table.fields_names_r for table in tables]

        new_matrix = join_base_from_start(
            matrices,connections,
            m_types,names_matrix)

        names = matrix.to_array(names_matrix)
        new_matrix.insert(0,array.get_formatted_words(names))

        new_matrix = get_matrix_with_removed_merged_columns(
            new_matrix,names_matrix,connections,m_types,names)

        result = Table(None,None,names,[],original=new_matrix)
        return result


    def get_all_connections(self,tables):
        """Returns connections betweeen tables
        and model types for each table."""
        m_types = [self.m_type]
        keys = [m_types[0].get_key_fields_names_and_types()]
        connections = []
        for tab in tables:
            tab_m_type = tab.m_type
            tab_keys = tab_m_type.get_key_fields_names_and_types()
            connection = find_connection_fields(keys,tab_keys,
                                                m_types,tab_m_type)
            connections.append(connection)
            m_types.append(tab_m_type)
            keys.append(tab_keys)
        return connections,m_types


def join_base(connections,types,
                other_types,names_matrix,
                other_names_matrix,
                entry,matrices):
    """Recursive algoritm that links tables."""
    if len(connections) == 0:
        return [entry]

    connection = connections[0]
    if connection is None:
        raise ImpossibleToJoinTables

    other_names = other_names_matrix[0]
    entries = try_connect_entry_with(connection,types,
        names_matrix,other_names,entry,matrices[0][1:])

    if entries is None:
        return []

    types.append(other_types[0])
    other_types = other_types[1:]
    connections = connections[1:]
    names_matrix.append(other_names_matrix[0])
    other_names_matrix = other_names_matrix[1:]

    result = []
    for _e in entries:
        result.extend(join_base(connections,types,
            other_types,names_matrix,other_names_matrix,
            _e,matrices[1:]))
    return result


def join_base_from_start(matrices,connections,
                         m_types,names_matrix):
    """The beginning of recursive algoritm that links tables."""
    _matrix = matrices[0]
    result = []
    for entry in _matrix[1:]:
        result.extend(join_base(connections,[m_types[0]],m_types[1:],
            [names_matrix[0]],names_matrix[1:],entry,matrices[1:]))
    return result


def find_connection_fields(keys_matrix,
                            keys_array,
                            types1,type2):
    """"Finds fields in 2 tables
    where one field is primary key,
    second field is foreign key of the same
    table."""
    for keys,type1 in zip(keys_matrix[::-1],types1[::-1]):
        for key1 in keys:
            if key1[1] == type2:
                key1[1] = [key1[1],type1]
                return key1

    for key2 in keys_array:
        if key2[1] in types1:
            return key2[::-1]

    raise ImpossibleToJoinTables


def try_connect_entry_with(connection,m_types,
                            names_matrix,other_names,
                            entry,other_matrix):
    """Tries to connect entry with table."""
    first_index,second_index,_ = \
        get_connection_indexes(
        connection,m_types,
        names_matrix,other_names)

    first = entry[first_index].number

    column = matrix.get_column(
        second_index,other_matrix)
    indexes = [_i for _i,element in \
        enumerate(column) if element.number == first]
    _matrix = array.get_rearranged_array(
        indexes,other_matrix)
    result = []
    for row in _matrix:
        res_row = entry.copy()
        res_row.extend(row)
        result.append(res_row)
    return result


def get_connection_indexes(connection,m_types,
                            names_matrix,other_names):
    """Returns first, second and real second
    connection indexes of columns."""
    if not isinstance(connection[0],str):
        first_type = connection[0]
        second_index = other_names.index(
            connection[1])
    else:
        first_type = connection[1][1]
        first_name = connection[0]
        second_index = 0

    subtable_index = m_types.index(first_type)
    first_index = sum(len(names) for names in \
        names_matrix[:subtable_index])

    if isinstance(connection[0],str):
        first_index += names_matrix[subtable_index]. \
            index(first_name)

    real_second_index = second_index \
        + sum(len(names) for names in names_matrix)
    return first_index,second_index,real_second_index


def get_all_connection_indexes(connections,m_types,
                                names_matrix):
    """Returns for each connection non-repeating
    first and real second indexes of columns."""
    indexes = set()
    for _i,connection in enumerate(connections):
        first_index,_,real_second_index = \
            get_connection_indexes(
            connection,m_types[:_i + 1],
            names_matrix[:_i + 1],names_matrix[_i + 1])
        indexes.add(first_index)
        indexes.add(real_second_index)
    indexes = list(indexes)
    return indexes


def get_matrices_with_foreigns_keys(
    connections,m_types,tables):
    """Returns matrices with columns of foreign keys that
    used in connections.
    Also changes source tables in the same way."""
    matrices = []
    for connection,table in zip( \
        connections,tables[1:]):
        if isinstance(connection[0],str):
            name = connection[0]
            t_index = m_types.index(connection[1][1])
            tables[t_index].add_fields_names([name])
        else:
            name = connection[1]
            table.add_fields_names([name])

    for table in tables:
        matrices = [table.get_matrix(of_fields=False) \
            for table in tables]
        table.fields_names_r.insert(0,"ID")

    return matrices


def get_matrix_with_removed_merged_columns(
    _matrix,names_matrix,connections,m_types,
    names):
    """Removes columns which were used for
    connection of tables. Returns new matrix."""
    columns = matrix.get_transposed_matrix(_matrix)
    indexes = get_all_connection_indexes(
        connections,m_types,names_matrix)
    indexes.sort(reverse=True)
    for index in indexes:
        del columns[index]
        del names[index]
    result = matrix.get_transposed_matrix(columns)
    return result


def get_table_by_name(t_name,full_access=True):
    """Returns one table by its
    name from this list: Admins,
    Appointments, Doctors, Patients,
    Shedules, Users, Vocations."""
    match t_name:
        case "Admins":
            ids = [entry.id for entry in models.Admin.select()]
            table = Table(
                ids,
                models.Admin,
                ["user"],
                ["user"],
                full_access)
        case "Appointments":
            ids = [entry.id for entry in models.Appointment.select()]
            table = Table(
                ids,
                models.Appointment,
                ["date","start","real_date","real_start",
                "real_end","patient","doctor","was_over"],
                ["date","start","real_date","real_start",
                "real_end","patient","doctor","was_over"],
                full_access)
        case "Doctors":
            ids = [entry.id for entry in models.Doctor.select()]
            table = Table(
                ids,
                models.Doctor,
                ["passport","date_of_birth","full_name",
                "place_of_residence","user","shedule",
                "vocation","cabinet","average_appointment_time"],
                ["passport","date_of_birth",
                "full_name","place_of_residence","user","shedule",
                "vocation","cabinet","average_appointment_time"],
                full_access)
        case "Patients":
            ids = [entry.id for entry in models.Patient.select()]
            table = Table(
                ids,
                models.Patient,
                ["passport","date_of_birth","full_name",
                "place_of_residence","user"],
                ["passport","date_of_birth","full_name",
                "place_of_residence","user"],
                full_access)
        case "Shedules":
            ids = [entry.id for entry in models.Shedule.select()]
            table = Table(
                ids,
                models.Shedule,
                ["days_in_week","start","lunch_start","lunch_end","end"],
                ["days_in_week","start","lunch_start","lunch_end","end"],
                full_access)
        case "Users":
            ids = [entry.id for entry in models.User.select()]
            table = Table(
                ids,
                models.User,
                ["email","password"],
                ["email","password"],
                full_access)
        case "Vocations":
            ids = [entry.id for entry in models.Vocation.select()]
            table = Table(
                ids,
                models.Vocation,
                ["name"],
                ["name"],
                full_access)
        case _:
            raise Exception(f"Table with name {t_name} doesn't exist.")
    return table
