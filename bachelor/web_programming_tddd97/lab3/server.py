from flask import Flask
from flask import request
from flask import jsonify, current_app
import database_helper
import re
import random
import os
from flask_sock import Sock
import json
from flask_bcrypt import Bcrypt
import hmac
import hashlib
import time
from datetime import timezone 
import datetime 
from datetime import datetime, timedelta


alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

app = Flask(__name__)
sock = Sock(app)
bcrypt = Bcrypt(app)

@app.teardown_request
def teardown(exception):
    database_helper.disconnect()

######################## Static Files #####################################

@app.route("/", methods=['GET'])
def get_index():
    return current_app.send_static_file('client.html')

@app.route("/<file>", methods=['GET'])
def get_index_js(file):
    return current_app.send_static_file(file)


############################################################################




active_connections = {}

@sock.route("/connect")
def connect(ws):
    token = request.args.get('token')
    etok = database_helper.validate_token(token)
    if etok == None:
        ws.close()
        return
    active_connections[etok['email']] = {
        "ws": ws,
        "token": etok['token']
    }
    try:
        while True:
            message = ws.receive()
            if message is None:
                break
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print("Received invalid JSON")
                continue
    except Exception as e:
        print("Exception error:", e)
    finally:
        conn = active_connections.get(etok['email'])
        if conn is not None and conn.get('token') == etok['token']:
            conn['ws'].close()
            active_connections.pop(etok['email'], None)






    

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

@app.route("/sign_up", methods=['POST'])
def sign_up():
    data = request.get_json()
    message = {}
    message['success'] = False
    if data is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if not data['email'] or  not data['password'] or  not data['firstname'] or  not data['familyname'] or  not data['gender'] or  not data['city'] or not data['country']:
        message['message'] = "Wrong form"
        return jsonify(message), 400
    if not valid_email(data['email']):
        message['message'] = "Not a valid email"
        return jsonify(message), 400
    if len(data['password']) < 5:
        message['message'] = "Password too short"
        return jsonify(message), 400
    if database_helper.get_user(data['email']) != None:
        message['message'] = "User already exsist"
        return jsonify(message), 409
    pw_hash = bcrypt.generate_password_hash(data['email'] + data['password']).decode('utf-8')
    if not database_helper.create_user(data['firstname'], data['familyname'], data['email'], data['country'], data['city'], data['gender'], pw_hash):
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Created user sucessfully"
    return jsonify(message), 201

def generate_token():
    token = ""
    for i in range(36):
        token += alph[random.randint(0, len(alph)-1)]
    return token

@app.route("/sign_in", methods=['POST'])
def sign_in():
    data = request.get_json()
    message = {}
    message['success'] = False

    if data is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if  not data['username'] or not data['password']:
        message['message'] = "missing email or password"
        return jsonify(message), 400
    if not valid_email(data['username']):
        message['message'] = "invalid email"
        return jsonify(message), 400
    if len(data['password']) < 5:
        message['message'] = "invalid email"
        return jsonify(message), 401
    
    hashed_pw = database_helper.get_password(data['username'])
    if hashed_pw == None:
        message['message'] = "invalid email or password"
        return jsonify(message), 401
    if bcrypt.check_password_hash(hashed_pw, data['username'] + data['password']) == False:
        message['message'] = "invalid email or password"
        return jsonify(message), 401
    token = generate_token()
    database_helper.delete_token(data['username'])
    conn = active_connections.get(data['username'])
    if conn is not None:
        try:
            ret = {}
            ret['action'] = 'sign_out'
            conn['ws'].send(json.dumps(ret))
            conn['ws'].close()
        except:
            pass
        active_connections.pop(data['username'], None)
    if database_helper.add_logged_in(data['username'],token) == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Login success"
    message['data'] = token
    return jsonify(message), 200

@app.route("/sign_out", methods=['DELETE'])
def sign_out():
    #data = request.get_json()
    #print(data)
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    '''if data is None:
        message['message'] = "No data"
        return jsonify(message)
        '''
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not database_helper.delete_token(etok['email']):
        message['message'] = "Server error"
        return jsonify(message), 500
    conn = active_connections.get(etok['email'])
    if conn is not None:
        try:
            ret = {}
            ret['action'] = 'sign_out'
            conn['ws'].send(json.dumps(ret))
            conn['ws'].close()
        except:
            pass
        active_connections.pop(etok['email'], None)
    message['success'] = True
    message['message'] = "sucessfully logged out"
    return jsonify(message), 200

@app.route("/change_password", methods=['PUT'])
def change_password():
    data = request.get_json()
    
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    
    if data is None or 'data' not in data or data['data'] is None:
        message['message'] = "No data"
        return jsonify(message), 400

    if auth_header is None:
        message['message'] = "Not logged in 1"
        return jsonify(message), 401

    etok = database_helper.validate_token(auth_header)
    if etok is None:
        message['message'] = "Not logged in 2"
        return jsonify(message), 401

    if not data["data"].get('oldpassword') or not data["data"].get('newpassword'):
        message['message'] = "No data"
        return jsonify(message), 400

    if len(data['data']['newpassword']) < 5:
        message['message'] = "Minimum password length = 5"
        return jsonify(message), 400

    if not data['data'].get('time'):
        message['message'] = "Old message"
        return jsonify(message), 401

    timestamp = datetime.fromisoformat(data['data']['time'].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
    current_time = datetime.now(timezone.utc)

    if current_time - timestamp > timedelta(minutes=1):
        message['message'] = "Old message"
        return jsonify(message), 401

    token = etok['token']
    json_message = json.dumps(data['data'], separators=(',', ':'))
    msg_hash = hmac.new(token.encode('utf-8'), json_message.encode('utf-8'), hashlib.sha256).hexdigest()

    print(etok['token'])
    print(data['data'])
    print(msg_hash)
    print(data['hash'])

    if msg_hash != data['hash']:
        message['message'] = "Invalid message 123"
        return jsonify(message), 401

    hashed_pw = database_helper.get_password(etok['email'])
    if hashed_pw is None:
        message['message'] = "Invalid email or password"
        return jsonify(message), 401

    if not bcrypt.check_password_hash(hashed_pw, etok['email'] + data['data']['oldpassword']):
        message['message'] = "Invalid email or password"
        return jsonify(message), 401

    pw_hash = bcrypt.generate_password_hash(etok['email'] + data['data']['newpassword']).decode('utf-8')  # Fixed the incorrect key lookup

    if not database_helper.set_password(etok['email'], pw_hash):
        message['message'] = "Server error"
        return jsonify(message), 500

    message['success'] = True
    message['message'] = "Changed password"
    return jsonify(message), 200


@app.route("/get_user_data_by_token", methods=['GET'])
def get_user_data_by_token():
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    ret = database_helper.get_user(etok['email'])
    if ret == None:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Retrieved user info"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/get_user_data_by_email/<email>", methods=['GET'])
def get_user_data_by_email(email):
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not valid_email(email):
        message['message'] = "Invalid email"
        return jsonify(message), 404
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    ret = database_helper.get_user(email)
    if ret == None:
        message['message'] = "User does not exist"
        return jsonify(message), 404
    message['success'] = True
    message['message'] = "Retrieved user info"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/get_user_messages_by_token/", methods=['GET'])
def get_user_messages_by_token():
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    ret = database_helper.get_posts(etok['email'])
    if ret is not None and ret == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/get_user_messages_by_email/<email>", methods=['GET'])
def get_user_messages_by_email(email):
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not valid_email(email):
        message['message'] = "Invalid email"
        return jsonify(message), 404
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if database_helper.get_user(email) == None:
        message['message'] = "User does not exist"
        return jsonify(message), 404
    ret = database_helper.get_posts(email)
    if ret is not None and ret == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/post_message", methods=['POST'])
def post_message():
    data = request.get_json()
    #print(data)
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if data is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not data['email'] or not data['message']:
        message['message'] = "Missing data"
        return jsonify(message), 400
    if data['message'] == "":
        message['message'] = "No message"
        return jsonify(message), 400
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not valid_email(data['email']):
        message['message'] = "Invalid email"
        return jsonify(message), 400
    if database_helper.get_user(data['email']) == None:
        message['message'] = "User does not exist"
        return jsonify(message), 400
    if not database_helper.create_post(etok['email'], data['email'], data['message']):
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Posted message"
    return jsonify(message), 201

if __name__ == '__main__':
    database_helper.init_db()
    app.debug = True
    app.run()
