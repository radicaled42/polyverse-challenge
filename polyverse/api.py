# api.py
import requests
import json

class PolyverseAPI: 
    def __init__(self, url, candidate_id):
        self.url = url
        self.candidate_id = candidate_id

    # Generate the api call
    def api_call(self, method, url, headers, payload):

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

    # Write an element on the external Polyverse
    def write_element_polyverse(self, element_data, binary_api):
        api = self.translate_api[f'{binary_api}']
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = json.dumps(element_data)
        headers = {
            'Content-Type': 'application/json'
        }
        return self.api_call("POST", url, headers, payload)

    # Delete an element from the external Polyverse
    def clean_element_poliverse(self, element_data, binary_api):
        api = self.translate_api[f'{binary_api}']
        url = f'{self.url}/{api}'
        element_data.update({"candidateId": self.candidate_id})
        payload = element_data
        headers = {}
        return self.api_call("DELETE", url, headers, payload)

    def translate_api(self, api_type):
        translate_api = {'0': 'polyanets', '1': 'soloons', '2': 'comeths'}
        return translate_api[api_type]
    
    # Get the external Polyverse map
    def get_polyverse_map(self):
        url = f'{self.url}/map/{self.candidate_id}'
        base_map = self.api_call("GET", url, {}, {})
        for row_index in range(0, len(base_map)):
            row_list = base_map[row_index]
            for col_index in range(0, len(row_list)):
                element = row_list[col_index]
                if element != None:
                    base_map[row_index][col_index]["action"] = 'NONE'
        return base_map
