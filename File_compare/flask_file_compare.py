from flask import Flask, jsonify, url_for, redirect, request
import file_compare_both_inputs_sorted as file
import json, secrets
from linecache import getline
application = Flask(__name__)
dictionary = {}
per_page = 2
@application.route('/paginate/', methods=["POST"])
def paginate():
    body_input = json.loads(request.data.decode())
    code = body_input["code"]
    num = int(body_input["page_number"])
    with open('output_files'+code+'.txt', 'r') as f:


    #return jsonify(dictionary[file1_address+file2_address][per_page*(num-1):per_page*(num)])
@application.route('/file_compare/', methods=['POST'])
def file_comp():
    code = secrets.token_hex(5)
    body_data = json.loads(request.data.decode())
    file1_address = body_data["file1_address"]
    file2_address = body_data["file2_address"]
    list3 = file.main_code(file1_address, file2_address)
    #dictionary[file1_address+file2_address] = list3
    #return jsonify(dictionary[file1_address+file2_address])
    file.listtofile(list3,code)
    return code


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)