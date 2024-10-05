import requests
import json
import time

colors = ['blue', 'red','purple','white']
direction = ['up', 'down', 'right', 'left']

'''
Polyverse Information
Based on challenge 2 the universe can mutate

Polyanets
row + column + candidateID

Soloons
row + column + color + candidateID
next to polyanets

Cometh
row + column + direction + candidateID
'''

class Polyverse:
    def __init__(self, url, candidate_id):
        self.url = url
        self.candidate_id = candidate_id
        self.map = self.getPolyverseMap()
    
    # Generate the api call
    def __api_call(self, method, url, headers, payload):

        try:
            response = requests.request(method, url, headers=headers, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(response.text)
        else:
            if response.status_code == 200:
                if method == 'POST' or method == 'DELETE':
                    print(f"Successful {method} Request")
                else:
                    data = response.json()
                    if 'goal' in url:
                        print("Got the Goal Map")
                        content = data.get('goal', None)
                    else:
                        print("Got the Map")
                        content = data.get('map', {}).get('content', None)
                    
                    if content is not None:
                        #print(content)
                        return content
            else:
                print(f"There was a problem with the request: code: {response.status_code}")

    # Get the external Polyverse map
    def getPolyverseMap(self):
        url = f'{self.url}/map/{self.candidate_id}'
        return self.__api_call("GET", url, {}, {})

    # Show the local Polyverse
    def showLocalPolyverse(self):
        for element in self.map:
            print(element)

    # Write an element on the external Polyverse
    def __writeElementPolyverse(self, element_data, api):
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = json.dumps(element_data)
        headers = {
            'Content-Type': 'application/json'
        }
        return self.__api_call("POST", url, headers, payload)

    # Delete an element from the external Polyverse
    def __cleanElementPoliverse(self, element_data, api):
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = element_data
        headers = {}
        return self.__api_call("DELETE", url, headers, payload)

    # Delete all the polyverse
    def cleanPolyverse(self):
        print ("Cleaning Polyverse")
        for row_index in range(0, len(self.map)):
            col_list = self.map[row_index]
            for col_index in range(0, len(col_list)):
                element = col_list[col_index]
                if element != None:
                    print (f'There is something there - {element} - row: {row_index} - col: {col_index}')
                    payload = element["payload"]
                    self.__cleanElementPoliverse({"row": row_index, "column": col_index}, payload["type"])

    # Write an element on the local Polyverse
    def writeLocalMap(self, element_data):
        if self.__verifyPosition(element_data, 'WRITE'):
            payload = element_data['payload']
            payload['action'] = 'WRITE'
            self.map[int(element_data['row'])][int(element_data['column'])] = payload
        else:
            print(f'There was a problem writing this element {element_data}')
        return
    
    # Delete an element from the local Polyverse
    def deleteLocalMap(self, element_data):
        if self.__verifyPosition(element_data, 'DELETE'):
            payload = element_data['payload']
            payload['action'] = 'DELETE'
            self.map[int(element_data['row'])][int(element_data['column'])] = payload
        else:
            print(f'There was a problem writing this element {element_data}')
        return
    
    # Merge Local into External Polyverse (Local --> External)
    def mergeMap(self):
        print("\nMerging Maps")
        polyverseMap = self.getPolyverseMap()
        # Compares local map with external mal
        for row_index in range(0, len(self.map)):
            col_list = self.map[row_index]
            for col_index in range(0, len(col_list)):
                element = col_list[col_index]
                # If local is different from external it overwrites it
                if element != polyverseMap[row_index][col_index]:
                    
                    # Sleep between requests
                    time.sleep(2)
                    
                    if element['action'] == 'DELETE': 
                        print (f'DELETE ACTION: {element} - row: {row_index} - col: {col_index}')
                        self.__cleanElementPoliverse({'row': str(row_index), 'column': str(col_index)}, element['type'])
                    else:
                        print (f'WRITE ACTION: {element} - row: {row_index} - col: {col_index}')
                        action_key = None
                        for key in element.keys():
                            if key != 'type' and key != 'action':
                                action_key = key
                                break
                        if action_key is not None:
                            payload = {'row': str(row_index), 'column': str(col_index), action_key: element[action_key]}
                        else: 
                            payload = {'row': str(row_index), 'column': str(col_index)}
                        self.__writeElementPolyverse(payload, element['type'])

    # Create payload for local map
    def local_map_payload(self, row, column, payload):
        match payload["type"]:
            case 'polyanets':
                return {"row": str(row), "column": str(column), "payload": {'type': 'polyanets'}}
            case 'soloons':
                return {"row": str(row), "column": str(column), "payload": {'type': 'soloons', 'color': payload['color']}}
            case 'comeths':
                return {"row": str(row), "column": str(column), "payload": {'type': 'comeths', 'direction': payload['direction']}}
            case _:
                print(f"ERROR: Unable to created payload for this element: {payload}")
                return -1

    def duplicatePolyverse(self, url):
        if url == None:
            url = f'{self.url}/map/{self.candidate_id}/goal'
        external_verse = self.__api_call('GET', url, {}, {})
  
        element_list = []

        # Translate the elements from goal map to local map
        for index_row in range(0, len(external_verse)):
            row_list = external_verse[index_row]
            for index_col in range(0, len(row_list)):
                element = row_list[index_col]
                if element != 'SPACE' and element != 'POLYANET':
                    other_element = element.split('_')
                    if other_element[1] == 'COMETH':
                        element_data = self.local_map_payload(index_row, index_col, {'type': 'comeths', 'direction': (other_element[0]).lower()})
                        element_list.append(element_data)
                    else:
                        element_data = self.local_map_payload(index_row, index_col, {'type': 'soloons', 'color': (other_element[0]).lower()})
                        element_list.append(element_data)
                elif element == 'POLYANET':
                    element_data = self.local_map_payload(index_row, index_col, {'type': 'polyanets'})
                    element_list.insert(0, element_data)

        # Write the translated elements on a local map
        for element in element_list:
            self.writeLocalMap(element)
        
        # Merge maps
        self.mergeMap()
        return
    
    # Check if its possible to write an element on the designated position
    def __verifyPosition(self, element_data, method):

        payload = element_data["payload"]
        # Check if this is a delete method
        if method == 'DELETE':
            return True
        match payload["type"]:
            case 'polyanets':
                return True
            case 'soloons':
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
                            if element["type"] == 'polyanets':
                                return True
                # If no matching element is found
                return False      
            case 'comeths':
                if "direction" in payload:
                    if payload["direction"] in direction:
                        return True
                return False
            case _:
                return False

             
#########################
### Support Functions ###
#########################
#def createHorizontalLineElement(pos_start, pos_end):
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


#def createVerticalLineElement(pos_start, pos_end):
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

def createDiagonalLineElement(pos_start, pos_end):
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

    #polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
    #test --> polyverse.writeElementPolyverse({"row": "1", "column": "1", "direction": "up"}, 'comeths')
    #test --> polyverse.cleanElementPoliverse({"row": "1", "column": "1"}, 'comeths')
    #polyverse.writeLocalMap({"row": "1", "column": "1", "payload": {"direction": "up", "type": "comeths"}})
    #polyverse.deleteLocalMap({"row": "1", "column": "1", "payload": {"type": "comeths"}})
    #polyverse.showLocalPolyverse()
    #polyverse.mergeMap()
    #print (polyverse.getPolyverseMap())
    #polyverse.cleanPolyverse()
    #polyverse.duplicatePolyverse()
    #polyverse.showPolyverse()

# Phase 1
#    polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
#    print("Show Polyverse: Inital definition")
#    polyverse.showPolyverse()
#    
#    for row, column in createDiagonalLineElement((2,2),(8,8)):
#        element_data = polyverse.local_map_payload(row, column, {'type': 'polyanets'})
#        polyverse.writeMap(element_data)
#        
#    for row, column in createDiagonalLineElement((8,2),(2,8)):
#        element_data = polyverse.local_map_payload(row, column, {'type': 'polyanets'})
#        polyverse.writeMap(element_data)
#    
#    print("\nShow Polyverse: Add Polyanets")
#    polyverse.showPolyverse()
#    polyverse.mergeMap()

# Phase 2
#    polyverse = Polyverse("https://test.com/api", "XXXXX-XXXX-XXXXX")
#    polyverse.duplicatePolyverse(None)
#    polyverse.showPolyverse()

main()