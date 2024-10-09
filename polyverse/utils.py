# utils.py
colors = ['blue', 'red','purple','white']
direction = ['up', 'down', 'right', 'left']

# Create payload for local map
def local_map_payload(self, row, column, payload):
    match payload["type"]:
        case 0:
            return {"row": str(row), "column": str(column), "payload": {'type': 0}}
        case 1:
            if 'color' not in payload.keys():
                print(f"ERROR: Unable to created payload for this element: {payload}")
                return None
            return {"row": str(row), "column": str(column), "payload": {'type': 1, 'color': payload['color']}}
        case 2:
            if 'direction' not in payload.keys():
                print(f"ERROR: Unable to created payload for this element: {payload}")
                return None
            return {"row": str(row), "column": str(column), "payload": {'type': 2, 'direction': payload['direction']}}
        case _:
            print(f"ERROR: Unable to created payload for this element: {payload}")
            return None
        
# Check if its possible to write an element on the designated position
def verify_position(self, element_data):

    payload = element_data["payload"]
    
    match payload["type"]:
        case 0:
            return True
        case 1:
            current_row = int(element_data["row"])
            current_col = int(element_data["column"])

             # Define row and column range (as per your provided structure)
            row_min = current_row - 1
            row_max = current_row + 1
            col_min = current_col - 1
            col_max = current_col + 1

             #print(f'Checking surroundings for row: {current_row}, col: {current_col}') 
            
            # Loop through the surrounding elements in the specified range
            for row_index in range(row_min, row_max + 1):
                for col_index in range(col_min, col_max + 1):
                    # Skip checking the current element itself
                    if row_index == current_row and col_index == current_col:
                        continue
                    # Access the element at the current surrounding position
                    element = self.map[row_index][col_index]
                    
                    # Check if the element is not None and matches the required condition
                    if element is not None:
                        if element["type"] == 0 and "color" in payload:
                            return True
            # If no matching element is found
            return False      
        case 2:
            if "direction" in payload:
                if payload["direction"] in direction:
                    return True
            return False
        case _:
            return False