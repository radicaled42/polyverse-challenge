import requests
import json
import time
import copy

colors = ['blue', 'red','purple','white']
direction = ['up', 'down', 'right', 'left']
translate_api = {'0': 'polyanets', '1': 'soloons', '2': 'comeths'}

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
        self.map = self.get_polyverse_map()
        return
        
    def __reset_map(self):
        self.map = self.get_polyverse_map()
        return
    
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
    def get_polyverse_map(self):
        url = f'{self.url}/map/{self.candidate_id}'
        base_map = self.__api_call("GET", url, {}, {})
        for row_index in range(0, len(base_map)):
            row_list = base_map[row_index]
            for col_index in range(0, len(row_list)):
                element = row_list[col_index]
                if element != None:
                    base_map[row_index][col_index]["action"] = 'NONE'
        return base_map

    # Show the local Polyverse
    def show_local_polyverse(self):
        copy_list = copy.deepcopy(self.map)
        
        for row_index in range(0, len(copy_list)):
            row_element = copy_list[row_index]
            for col_index in range(0, len(row_element)):
                element = row_element[col_index]
                # Simplify Map for print
                if element == None:
                    copy_list[row_index][col_index] = '-'
                else:
                    element_type = element["type"]
                    match element_type:
                        case 0:
                            copy_list[row_index][col_index] = 'P'
                        case 1:
                            copy_list[row_index][col_index] = 'S'
                        case 2:
                            copy_list[row_index][col_index] = 'C'
        for element in copy_list:
            print(''.join(element))
        return copy_list

    # Write an element on the external Polyverse
    def __write_element_polyverse(self, element_data, binary_api):
        api = translate_api[f'{binary_api}']
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = json.dumps(element_data)
        headers = {
            'Content-Type': 'application/json'
        }
        return self.__api_call("POST", url, headers, payload)

    # Delete an element from the external Polyverse
    def __clean_element_poliverse(self, element_data, binary_api):
        api = translate_api[f'{binary_api}']
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = element_data
        headers = {}
        return self.__api_call("DELETE", url, headers, payload)

    # Delete all the polyverse
    def clean_polyverse(self):
        print ("Cleaning Polyverse - START")
        for row_index in range(0, len(self.map)):
            col_list = self.map[row_index]
            for col_index in range(0, len(col_list)):
                element = col_list[col_index]
                if element != None:
                    print (f'There is something there - {element} - row: {row_index} - col: {col_index}')
                    self.__clean_element_poliverse({"row": row_index, "column": col_index}, element["type"])
                    
                    # Sleep between requests
                    time.sleep(2)
        print ("Cleaning Polyverse - END")
        return

    # Write an element on the local Polyverse
    def write_local_map(self, element_data):
        if self.__verify_position(element_data):
            payload = element_data['payload']
            payload['action'] = 'WRITE'
            self.map[int(element_data['row'])][int(element_data['column'])] = payload
        else:
            print(f'There was a problem writing this element {element_data}')
            return -1
        return 1
    
    # Delete an element from the local Polyverse
    def delete_local_map(self, element_data):

        payload = element_data['payload']
        payload['action'] = 'DELETE'
        
        map_element = self.map[int(element_data['row'])][int(element_data['column'])]
        
        if map_element is not None and map_element['action'] == 'NONE':
            self.map[int(element_data['row'])][int(element_data['column'])] = payload
        elif map_element is not None and map_element['action'] == 'WRITE':
            self.map[int(element_data['row'])][int(element_data['column'])] = None
        return 1
    
    # Merge Local into External Polyverse (Local --> External)
    def merge_map(self):
        action_results = []
        
        print("\nMerging Maps")
        
        # Get external map
        polyverseMap = self.get_polyverse_map()
        
        # Compares local map with external map
        for row_index in range(0, len(self.map)):
            col_list = self.map[row_index]
            for col_index in range(0, len(col_list)):
                element = col_list[col_index]
                
                # Remove action for comparison
                element_filtered = None if element == None else {k: v for k, v in element.items() if k != 'action'}
                polyverse_filtered = None if polyverseMap[row_index][col_index] == None else {k: v for k, v in polyverseMap[row_index][col_index].items() if k != 'action'}
                # If local is different from external it overwrites it
                if element_filtered != polyverse_filtered:
                    
                    # Sleep between requests
                    time.sleep(2)
                    
                    # Check if this is a WRITE/DELETE action
                    if element['action'] == 'DELETE': 
                        print (f'DELETE ACTION: {element} - row: {row_index} - col: {col_index}')
                        api_result = self.__clean_element_poliverse({'row': str(row_index), 'column': str(col_index)}, element['type'])
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
                        api_result = self.__write_element_polyverse(payload, element['type'])
                    action_results.append(api_result)
                #else:
                #    print (f"The element {element} - row: {row_index} - col: {col_index} its already on the external map")
        
        # Reset map to have the latest version          
        self.__reset_map()
        
        return list(set(action_results))

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

    def duplicate_polyverse(self, url):
        print("Duplicate Polyverse - START")
        
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
                        element_data = self.local_map_payload(index_row, index_col, {'type': 2, 'direction': (other_element[0]).lower()})
                        element_list.append(element_data)
                    else:
                        element_data = self.local_map_payload(index_row, index_col, {'type': 1, 'color': (other_element[0]).lower()})
                        element_list.append(element_data)
                elif element == 'POLYANET':
                    element_data = self.local_map_payload(index_row, index_col, {'type': 0})
                    element_list.insert(0, element_data)

        # Write the translated elements on a local map
        for element in element_list:
            self.write_local_map(element)
        
        # Merge maps
        merge_result = self.merge_map()
        
        print("Duplicate Polyverse - END")
        return merge_result
    
    # Check if its possible to write an element on the designated position
    def __verify_position(self, element_data):

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
