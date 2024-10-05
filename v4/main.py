from polyverse import Polyverse
from flask import Flask, request, jsonify
import os

#########################
### Support Functions ###
#########################
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
        

# Initialize the Flask app
app = Flask(__name__)

# Get configuration from environment variables with defaults
POLYVERSE_URL = os.getenv('POLYVERSE_URL', 'https://test.com/api')
CANDIDATE_ID = os.getenv('CANDIDATE_ID', 'XXXXX-XXXX-XXXXX')

# Initialize Polyverse instance with environment variables
polyverse = Polyverse(POLYVERSE_URL, CANDIDATE_ID)

# Route for showing the Polyverse
@app.route('/show', methods=['GET'])
def show_local():
    local_map = polyverse.show_local_polyverse()
    app.logger.info('/show - Showing local map')
    return jsonify({"message": "Element written successfully!", "local_map": local_map}), 200

# Route for cleaning the Polyverse
@app.route('/clean', methods=['POST'])
def clean_polyverse():
    polyverse.clean_polyverse()
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
            element_data = polyverse.local_map_payload(row, column, data['payload'])
            polyverse.write_local_map(element_data)
    else:
        element_data = polyverse.local_map_payload(start[0], start[1], data['payload'])
        polyverse.write_local_map(element_data)
        
    merge_result = polyverse.merge_map()
    if -1 in merge_result:
        app.logger.error('/write - There was a problem with the writing action check the logs')
        return jsonify({"message": "There was a problem with the writing action check the logs", "local_map": local_map}), 400
        
    local_map = polyverse.show_local_polyverse()

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
            polyverse.delete_local_map({"row": row, "column": column, "payload": data['payload']})
            
    else:
        polyverse.delete_local_map({"row": start[0], "column": start[1], "payload": data['payload']})
        
    merge_result = polyverse.merge_map()
    if -1 in merge_result:
        app.logger.error('/delete - There was a problem with the delete action check the logs')
        return jsonify({"message": "There was a problem with the delete action check the logs", "local_map": local_map}), 400
        
    local_map = polyverse.show_local_polyverse()

    app.logger.info('/delete - Delete action completed successfully')
    return jsonify({"message": "Delete action completed successfully!", "local_map": local_map}), 200

# Route for duplicating external Polyverse
@app.route('/duplicate', methods=['POST'])
def duplicate_map():
    data = request.json  # Get the data from the request body (assuming it's JSON)

    url = data[url] if 'url' in data.keys() else None
    duplication_results = polyverse.duplicate_polyverse(url)
    
    if -1 in duplication_results:
        app.logger.error('/duplication - There was a problem with the duplication action check the logs')
        return jsonify({"message": "There was a problem with the duplication action check the logs", "local_map": local_map}), 400
        
    local_map = polyverse.show_local_polyverse()

    app.logger.info('/write - Writing action completed successfully')
    return jsonify({"message": "Writing action completed successfully!", "local_map": local_map}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)