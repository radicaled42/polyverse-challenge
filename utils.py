# utils.py

def create_horizontal_line_element(pos_start, pos_end):
    init_row, init_col = pos_start
    end_row, end_col = pos_end

    elements = []
    if isinstance(init_col, int) and isinstance(end_col, int) and 0 <= init_col <= 10 and 0 <= end_col <= 10:
        if init_col > end_col:
            init_col, end_col = end_col, init_col
    else:
        print ("There is a problem with the Columns")
        return

    if isinstance(init_row, int) and isinstance(end_row, int) and init_row != end_row:
        print("There is aproblem with the Rows")
        return

    for col_index in range (init_col, end_col + 1):
        elements.append((init_row, col_index))

    #print (elements)
    return elements


def create_vertical_line_element(pos_start, pos_end):
    init_row, init_col = pos_start
    end_row, end_col = pos_end

    elements = []

    if isinstance(init_row, int) and isinstance(end_col, int) and 0 <= init_row <= 10 and 0 <= end_col <= 10:
        if init_row > end_col:
            init_row, end_col = end_col, init_row
    else:
        print ("There is a problem with the Columns")
        return

    if isinstance(init_col, int) and isinstance(end_col, int) and init_col != end_col:
        print("There is aproblem with the Columns")
        return

    for row_index in range (init_row, end_row + 1):
        elements.append((row_index, init_col))

    #print (elements)
    return elements

def create_diagonal_line_element(pos_start, pos_end):
    init_row, init_col = pos_start
    end_row, end_col = pos_end

    elements = []

     # Check if the line is a valid diagonal (same number of row and column steps)
    if abs(end_row - init_row) == abs(end_col - init_col):
        row_step = 1 if end_row > init_row else -1
        col_step = 1 if end_col > init_col else -1

         # Iterate diagonally from pos_start to pos_end
        for i in range(abs(end_row - init_row) + 1):
            elements.append((init_row + i * row_step, init_col + i * col_step))
    else:
        print("Invalid diagonal: The number of rows and columns steps must be equal.")

    #print(elements)
    return elements

def get_elements(pos_start, pos_end):
    init_row, init_col = pos_start
    end_row, end_col = pos_end
    
    if abs(init_row - end_row) == abs(init_col - end_col):
        return create_diagonal_line_element(pos_start, pos_end)
    elif init_row == end_row:
        return create_horizontal_line_element(pos_start, pos_end)
    elif init_col == end_col:
        return create_vertical_line_element(pos_start, pos_end)
        