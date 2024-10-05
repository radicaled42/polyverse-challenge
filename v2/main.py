from polyverse import Polyverse

#########################
### Support Functions ###
#########################
#def create_horizontal_line_element(pos_start, pos_end):
#    init_row, init_col = pos_start
#    end_row, end_col = pos_end
#
#    elements = []
#    if isinstance(init_col, int) and isinstance(end_col, int) and 0 <= init_col <= 10 and 0 <= end_col <= 10:
#        if init_col > end_col:
#            init_col, end_col = end_col, init_col
#    else:
#        print ("There is a problem with the Columns")
#        return
#
#    if isinstance(init_row, int) and isinstance(end_row, int) and init_row != end_row:
#        print("There is aproblem with the Rows")
#        return
#
#    for col_index in range (init_col, end_col + 1):
#        elements.append((init_row, col_index))
#
#    #print (elements)
#    return elements


#def create_vertical_line_element(pos_start, pos_end):
#    init_row, init_col = pos_start
#    end_row, end_col = pos_end
#
#    elements = []
#
#    if isinstance(init_row, int) and isinstance(end_col, int) and 0 <= init_row <= 10 and 0 <= end_col <= 10:
#        if init_row > end_col:
#            init_row, end_col = end_col, init_row
#    else:
#        print ("There is a problem with the Columns")
#        return
#
#    if isinstance(init_col, int) and isinstance(end_col, int) and init_col != end_col:
#        print("There is aproblem with the Columns")
#        return
#
#    for row_index in range (init_row, end_row + 1):
#        elements.append((row_index, init_col))
#
#    #print (elements)
#    return elements

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

## Main
def main():
    pass

## Method Usage
#    polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
#    # Write an element of the local Map
#    # Needs a dict {"row": <ROW_POSITION>, "column": <COLUMN_POSITION>, "payload": {<COLOR/DIRECTION>, "type": <TYPE_ELEMENT>}}
#    #polyverse.write_local_map({"row": "1", "column": "1", "payload": {"direction": "up", "type": "comeths"}})
#    polyverse.write_local_map({"row": "1", "column": "1", "payload": {"direction": "up", "type": 2}})
#    # Delete an element of the local Map
#    # Needs a dict {"row": <ROW_POSITION>, "column": <COLUMN_POSITION>, "payload": {"type": <TYPE_ELEMENT>}}
#    #polyverse.delete_local_map({"row": "1", "column": "1", "payload": {"type": "comeths"}})
#    polyverse.delete_local_map({"row": "1", "column": "1", "payload": {"type": 2}})
#    # Beaufy print of the Polyverse
#    polyverse.show_local_polyverse()
#    # Merge de local map with the online one
#    polyverse.merge_map()
#    # Remove all the element of the Polyverse
#    polyverse.clean_polyverse()
#    # Duplicates a polyverse (you can provide the URL or it can autogenerate from the candidate info)
#    polyverse.duplicate_polyverse(None)
#    # Reset map with the latest version
#    polyverse.reset_local_map()

#
## Phase 1
#    polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
#    print("Show Polyverse: Inital definition")
#    polyverse.show_local_polyverse()
#    
#    for row, column in create_diagonal_line_element((2,2),(8,8)):
#        element_data = polyverse.local_map_payload(row, column, {'type': 0})
#        polyverse.write_local_map(element_data)
#        
#    for row, column in create_diagonal_line_element((8,2),(2,8)):
#        element_data = polyverse.local_map_payload(row, column, {'type': 0})
#        polyverse.write_local_map(element_data)
#    
#    print("\nShow Polyverse: Add Polyanets")
#    polyverse.show_local_polyverse()
#    polyverse.merge_map()
#
## Phase 2
#    polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
#    polyverse.duplicate_polyverse(None)
#    polyverse.show_local_polyverse()

if __name__ == "__main__":
    main()