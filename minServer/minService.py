from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/hosts', methods=['GET','POST'])
#ToDo: This end point needs to check if the host already exists.
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data=request.get_json()
        HOSTS.append({
            'id': uuid.uuid4().hex,
            'ipaddress': post_data.get('ipaddress'),
            'computer_name': post_data.get('computer_name'),
            'minknow_version': post_data.get('minknow_version')
        })
        response_object['message'] = "Host added!"
    else:
        response_object['hosts'] = HOSTS
    return jsonify(response_object)

def remove_host(host_id):
    for host in HOSTS:
        if host['id'] == host_id:
            HOSTS.remove(host)
            return True
    return False

@app.route('/hosts/<host_id>', methods=['PUT', 'DELETE'])
def single_host(host_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_host(host_id)
        HOSTS.append({
            'id': uuid.uuid4().hex,
            'ipaddress': post_data.get('ipaddress'),
            'computer_name': post_data.get('computer_name'),
            'minknow_version': post_data.get('minknow_version')
        })
        response_object['message'] = 'Host updated!'
    if request.method == 'DELETE':
        remove_host(host_id)
        response_object['message'] = 'Host removed!'
    return jsonify(response_object)

HOSTS = [
]

if __name__ == '__main__':
    print ("Getting ready to go")
    app.run(host ='192.168.1.68')
