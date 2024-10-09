from flask import Flask, request, jsonify
import os
from utils import get_elements
from polyverse.api import PolyverseAPI
from polyverse.map_handler import MapHandler

# Initialize the Flask app
app = Flask(__name__)

# Get configuration from environment variables with defaults
POLYVERSE_URL = os.getenv('POLYVERSE_URL', 'https://test.com/api')
CANDIDATE_ID = os.getenv('CANDIDATE_ID', 'XXXXX-XXXX-XXXXX')

# Initialize PolyverseAPI and MapHandler instances
polyverse_api = PolyverseAPI(POLYVERSE_URL, CANDIDATE_ID)
map_handler = MapHandler(polyverse_api)

# Route for showing the Polyverse
@app.route('/show', methods=['GET'])
def show_local():
    local_map = map_handler.show_local_polyverse()
    app.logger.info('/show - Showing local map')
    return jsonify({"message": "Element written successfully!", "local_map": local_map}), 200

# Route for cleaning the Polyverse
@app.route('/clean', methods=['POST'])
def clean_polyverse():
    map_handler.api.clean_polyverse()
    app.logger.info('/clean - Cleaning action completed successfully')
    return jsonify({"message": "Cleaning action completed successfully!"}), 200

# Route for writing in the Polyverse
@app.route('/write', methods=['POST'])
def write_map():
    data = request.json  # Get the data from the request body (assuming it's JSON)
    
    if 'start' not in data.keys():
        app.logger.error('/write - Missing start values unable to continue')
        return jsonify({"message": "Missing start values unable to continue"}), 400
    
    start = eval(data['start'])
    if 'end' in data.keys():
        end = eval(data['end'])
        for row, column in get_elements(start,end):
            element_data = map_handler.local_map_payload(row, column, data['payload'])
            map_handler.write_local_map(element_data)
    else:
        element_data = map_handler.local_map_payload(start[0], start[1], data['payload'])
        map_handler.write_local_map(element_data)
        
    merge_result = map_handler.merge_map()
    if -1 in merge_result:
        app.logger.error('/write - There was a problem with the writing action check the logs')
        return jsonify({"message": "There was a problem with the writing action check the logs", "local_map": local_map}), 400
        
    local_map = map_handler.show_local_polyverse()

    app.logger.info('/write - Writing action completed successfully')
    return jsonify({"message": "Writing action completed successfully!", "local_map": local_map}), 200

# Route for deleting in the Polyverse
@app.route('/delete', methods=['DELETE'])
def delete_map():
    data = request.json  # Get the data from the request body (assuming it's JSON)
    
    if 'start' not in data.keys():
        app.logger.error('/delete - Missing start values unable to continue')
        return jsonify({"message": "Missing start values unable to continue"}), 400
    
    start = eval(data['start'])
    if 'end' in data.keys():
        end = eval(data['end'])
        for row, column in get_elements(start,end):
            map_handler.delete_local_map({"row": row, "column": column, "payload": data['payload']})
            
    else:
        map_handler.delete_local_map({"row": start[0], "column": start[1], "payload": data['payload']})
        
    merge_result = map_handler.merge_map()
    if -1 in merge_result:
        app.logger.error('/delete - There was a problem with the delete action check the logs')
        return jsonify({"message": "There was a problem with the delete action check the logs", "local_map": local_map}), 400
        
    local_map = map_handler.show_local_polyverse()

    app.logger.info('/delete - Delete action completed successfully')
    return jsonify({"message": "Delete action completed successfully!", "local_map": local_map}), 200

# Route for duplicating external Polyverse
@app.route('/duplicate', methods=['POST'])
def duplicate_map():
    data = request.json  # Get the data from the request body (assuming it's JSON)

    url = data[url] if 'url' in data.keys() else None
    duplication_results = map_handler.duplicate_polyverse(url)
    
    if -1 in duplication_results:
        app.logger.error('/duplication - There was a problem with the duplication action check the logs')
        return jsonify({"message": "There was a problem with the duplication action check the logs", "local_map": local_map}), 400
        
    local_map = map_handler.show_local_polyverse()

    app.logger.info('/write - Writing action completed successfully')
    return jsonify({"message": "Writing action completed successfully!", "local_map": local_map}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)