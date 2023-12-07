"""Operations with matrix.
Matrix is 2D array.
Entry matrix[_i][_j] means addressing
to the element of matrix with _i row and
_j column."""
import re
from modules import o_array


def get_matrix_with_inner_borders(matrix):
    """Returns matrix with inner separators as elements."""
    result = [o_array.join_to_array(" | ",row) \
        for row in matrix]

    row_separator = get_horizontal_separator(matrix)
    result = o_array.join_to_array(row_separator,result)
    return result


def get_rows_count(matrix):
    """Returns rows count in the matrix."""
    rows_count = len(matrix)
    return rows_count


def get_assembled_matrix(matrix):
    """Returns the multiline text being
    assembled rows."""
    str_matrix = get_matrix_with_str_elements(matrix)
    assembled_rows = [o_array.get_assembled_array(row) \
        for row in str_matrix]
    result = '\n'.join(assembled_rows)
    return result


def get_matrix_with_str_elements(matrix):
    """Returns matrix where all elements converted to string."""
    result = [[str(elem) for elem in row] for row in matrix]
    return result


def get_columns_count(matrix):
    """Returns columns count in the matrix."""
    columns_count = len(matrix[0])
    return columns_count


def get_transposed_matrix(matrix):
    """Returns transposed matrix."""
    columns_count = \
        get_columns_count(matrix)

    return [get_column(index,matrix) \
        for index in range(columns_count)]


def get_column(column_index,matrix):
    """Returns column of matrix with
    specified index."""
    column = [row[column_index] for row in matrix]
    return column


def get_horizontal_separator(matrix):
    """Returns a divided horizontal separator."""
    row = matrix[0]
    result = [re.sub('.','-',element) for element in row]
    result = o_array.join_to_array('-+-',result)
    return result


def get_rjusted_matrix(matrix):
    """Returns matrix with right justified
    columns."""
    columns = get_transposed_matrix(matrix)
    rjusted_columns = [o_array.\
        get_rjusted_column(column) \
        for column in columns]

    matrix = get_transposed_matrix(rjusted_columns)
    return matrix


def get_matrix_as_text(matrix):
    """Prepares matrix for print."""
    rjusted_matrix = get_rjusted_matrix(matrix)

    matrix_with_inner_borders = \
    get_matrix_with_inner_borders(rjusted_matrix)

    result = get_assembled_matrix( \
    matrix_with_inner_borders)
    return result


def get_sorted_matrix(matrix,column_index,reverse=False):
    """Returns matrix sorted by column.
    Note that the firts row of matrix
    consists of columns names."""

    matrix_header = matrix[0]
    result = matrix[1:]
    result.sort(reverse=reverse,key=lambda row: row[column_index])
    result.insert(0,matrix_header)
    return result


def search_in_matrix(matrix,column_index,regular_expression):
    """Searches rows in the matrix where for each row
    there is the element that matches specified column 
    and partly matches regular expression.
    Returns matrix of this rows.
    Note that the firts row of matrix
    consists of columns names."""

    matrix_header = matrix[0]
    matrix_body = matrix[1:]
    column = get_column(column_index,matrix_body)

    indexes = o_array.search_elements(regular_expression,column)
    result = o_array.get_rearranged_array(indexes,matrix_body)
    result.insert(0,matrix_header)
    return result


def filter_matrix(matrix,column_index,start,end):
    """Searches rows in the matrix where for each row
    there is the element that matches specified column 
    and less than or equal to "end",
    great than or equal to "start".
    Returns matrix of this rows.
    Note that the firts row of matrix
    consists of columns names."""

    matrix_header = matrix[0]
    matrix_body = matrix[1:]
    column = get_column(column_index,matrix_body)

    indexes = o_array.filter_elements(start,end,column)
    result = o_array.get_rearranged_array(indexes,matrix_body)
    result.insert(0,matrix_header)
    return result


def to_array(matrix):
    """Combines all rows into one."""
    result = []
    for row in matrix:
        result.extend(row)
    return result
