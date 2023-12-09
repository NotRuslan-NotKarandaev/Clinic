"""Operations with arrays."""
import re


def join_to_array(joined_element,array):
    """Returns array that consists of the elements
    of the source array separated by joined elements."""
    result = []
    for index,element in enumerate(array):
        result.append(element)
        if index < get_last_index(array):
            result.append(joined_element)

    return result


def get_last_index(array):
    """Returns the last index in the array."""
    return len(array) - 1


def get_max_length(array):
    """Returns maximum length of
    elements in the array."""
    elements_lengths = \
        map(lambda element: len(str(element)),array)
    return max(elements_lengths)


def are_objects_arrays(objects):
    """Checks if objects are arrays."""
    for obj in objects:

        if not isinstance(obj,list):
            return False

    return True


def are_arrays_len_equal(arrays):
    """Checks if arrays lengths are the same."""
    arrays = list(arrays)
    array1 = arrays[0]

    for array2 in arrays[1:]:

        if not are_arrays_len_equal_base(array1,array2):
            return False

        array1 = array2

    return True


def are_arrays_len_equal_base(array1,array2):
    """Checks if the two arrays lengths are the same."""
    return len(array1) == len(array2)


def are_arrays_equal(array1,array2):
    """Checks if the two arrays are the same."""
    if not are_arrays_len_equal_base(array1,array2):
        return False
    for pair in zip(array1,array2):
        if pair[0] != pair[1]:
            return False
    return True


def get_assembled_array(array):
    """Returns the string being the concatenation
    of all elements in the array.
    Elements must be strings."""
    result = ''.join(array)
    return result


def get_range_inclusive(start,end,step = 1):
    """Returns range from start to end inclusive."""
    return range(start,end+1,step)


def get_rjusted_column(column):
    """Returns column with right justified
    elements casted to strings."""
    column_width = get_max_length(column)
    return list(map( \
        lambda elem: str(elem).rjust(column_width), \
        column))


def search_elements(regular_expression,
                    array):
    """Searches elements in array
    that partly matches regular expression.
    Returns their indexes in the array."""
    result = []
    for index,elem in enumerate(array):
        if re.search(regular_expression, \
            str(elem)) is not None:
            result.append(index)
    return result


def filter_elements(start,end,
                    array):
    """Filtres elements in array
    which are in range from the start
    to the end.
    Returns their indexes in the array."""
    result = []
    for index,elem in enumerate(array):
        if elem.is_in_range_inclusive( \
            start,end):
            result.append(index)
    return result


def get_rearranged_array(indexes,array):
    """Gets array with changed positions of
    elements in accordance of their new indexes."""
    result = [array[index] for index in indexes]
    return result


def get_formatted_words(words):
    """Returns array of words where
    the first letters are capital and
    all underscores are substituted with spaces."""
    words = words.copy()
    for _i,word in enumerate(words):
        word = word.replace("_"," ")
        words[_i] = word[0].upper() + word[1:]
    return words
