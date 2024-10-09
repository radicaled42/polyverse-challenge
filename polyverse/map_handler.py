
import time
import copy

from polyverse.utils import local_map_payload, verify_position

class MapHandler:
    def __init__(self, api):
        self.api = api
        self.map = self.api.get_polyverse_map()
        
    def __reset_map(self):
        self.map = self.api.get_polyverse_map()
        return
    
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
        if verify_position(element_data):
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
        polyverseMap = self.api.get_polyverse_map()
        
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
                        api_result = self.api.clean_element_poliverse({'row': str(row_index), 'column': str(col_index)}, element['type'])
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
                        api_result = self.api.write_element_polyverse(payload, element['type'])
                    action_results.append(api_result)
                #else:
                #    print (f"The element {element} - row: {row_index} - col: {col_index} its already on the external map")
        
        # Reset map to have the latest version          
        self.__reset_map()
        
        return list(set(action_results))

    def duplicate_polyverse(self, url):
        print("Duplicate Polyverse - START")
        
        if url == None:
            url = f'{self.url}/map/{self.candidate_id}/goal'
        external_verse = self.api.api_call('GET', url, {}, {})
  
        element_list = []

        # Translate the elements from goal map to local map
        for index_row in range(0, len(external_verse)):
            row_list = external_verse[index_row]
            for index_col in range(0, len(row_list)):
                element = row_list[index_col]
                if element != 'SPACE' and element != 'POLYANET':
                    other_element = element.split('_')
                    if other_element[1] == 'COMETH':
                        element_data = local_map_payload(index_row, index_col, {'type': 2, 'direction': (other_element[0]).lower()})
                        element_list.append(element_data)
                    else:
                        element_data = local_map_payload(index_row, index_col, {'type': 1, 'color': (other_element[0]).lower()})
                        element_list.append(element_data)
                elif element == 'POLYANET':
                    element_data = local_map_payload(index_row, index_col, {'type': 0})
                    element_list.insert(0, element_data)

        # Write the translated elements on a local map
        for element in element_list:
            self.write_local_map(element)
        
        # Merge maps
        merge_result = self.merge_map()
        
        print("Duplicate Polyverse - END")
        return merge_result

