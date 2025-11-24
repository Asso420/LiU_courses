from flask import Flask
from flask import request
from flask import jsonify
import database_helper
import re
import random
import os
alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

app = Flask(__name__)

@app.teardown_request
def teardown(exception):
    database_helper.disconnect()

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

@app.route("/sign_up", methods=['POST'])
def sign_up():
    data = request.get_json()
    message = {}
    message['success'] = False
    if data is None:
        message['message'] = "No data"
        return jsonify(message)
    if not data['email'] or  not data['password'] or  not data['firstname'] or  not data['familyname'] or  not data['gender'] or  not data['city'] or not data['country']:
        message['message'] = "Wrong form"
        return jsonify(message)
    if not valid_email(data['email']):
        message['message'] = "Not a valid email"
        return jsonify(message)
    if len(data['password']) < 5:
        message['message'] = "Password too short"
        return jsonify(message)
    if database_helper.get_user(data['email']) != None:
        message['message'] = "User already exsist"

    if not database_helper.create_user(data['firstname'], data['familyname'], data['email'], data['country'], data['city'], data['gender'], data['password']):
        message['message'] = "Server error"
        return jsonify(message)
    message['success'] = True
    message['message'] = "Created user sucessfully"
    return jsonify(message)

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
        return jsonify(message)
    if  not data['username'] or not data['password']:
        message['message'] = "missing email or password"
        return jsonify(message)
    if not valid_email(data['username']):
        message['message'] = "invalid email"
        return jsonify(message)
    if len(data['password']) < 5:
        message['message'] = "invalid email"
        return jsonify(message)
    if database_helper.valid_password(data['username'], data['password']) == False:
        message['message'] = "invalid email or password"
        return jsonify(message)
    token = generate_token()
    if database_helper.add_logged_in(data['username'],token) == False:
        message['message'] = "Server error"
        return jsonify(message)
    message['success'] = True
    message['message'] = "Login success"
    message['data'] = token
    return jsonify(message)

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
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not database_helper.delete_token(etok['email']):
        message['message'] = "Server error"
        return jsonify(message)
    message['success'] = True
    message['message'] = "sucessfully logged out"
    return jsonify(message)

@app.route("/change_password", methods=['PUT'])
def change_password():
    data = request.get_json()
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if data is None:
        message['message'] = "No data"
        return jsonify(message)
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not data['oldpassword'] or not data['newpassword']:
        message['message'] = "No data"
        return jsonify(message)
    if len(data['newpassword']) < 5:
        message['message'] = "Minimum password length = 5"
        return jsonify(message)
    if database_helper.valid_password(etok['email'] , data['oldpassword']) == False:
       message['message'] = "invalid password"
       return jsonify(message)
    if database_helper.set_password(etok['email'], data['newpassword']) == False:
       message['message'] = "Server error"
       return jsonify(message)
    message['success'] = True
    message['message'] = "Changed password"
    return jsonify(message)

@app.route("/get_user_data_by_token", methods=['GET'])
def get_user_data_by_token():
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    ret = database_helper.get_user(etok['email'])
    if ret == None:
        message['message'] = "Server error"
        return jsonify(message)
    message['success'] = True
    message['message'] = "Retrieved user info"
    message['data'] = ret
    return jsonify(message)

@app.route("/get_user_data_by_email/<email>", methods=['GET'])
def get_user_data_by_email(email):
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not valid_email(email):
        message['message'] = "Invalid email"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    ret = database_helper.get_user(email)
    if ret == None:
        message['message'] = "User does not exist"
        return jsonify(message)
    message['success'] = True
    message['message'] = "Retrieved user info"
    message['data'] = ret
    return jsonify(message)

@app.route("/get_user_messages_by_token/", methods=['GET'])
def get_user_messages_by_token():
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    ret = database_helper.get_posts(etok['email'])
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message)

@app.route("/get_user_messages_by_email/<email>", methods=['GET'])
def get_user_messages_by_email(email):
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not valid_email(email):
        message['message'] = "Invalid email"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if database_helper.get_user(email) == None:
        message['message'] = "User does not exist"
        return jsonify(message)
    ret = database_helper.get_posts(email)
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message)

@app.route("/post_message", methods=['POST'])
def post_message():
    data = request.get_json()
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if data is None:
        message['message'] = "No data"
        return jsonify(message)
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not data['email'] or not data['message']:
        message['message'] = "Missing data"
        return jsonify(message)
    if data['message'] == "":
        message['message'] = "No message"
        return jsonify(message)
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message)
    if not valid_email(data['email']):
        message['message'] = "Invalid email"
        return jsonify(message)
    if database_helper.get_user(data['email']) == None:
        message['message'] = "User does not exist"
        return jsonify(message)
    if not database_helper.create_post(etok['email'], data['email'], data['message']):
        message['message'] = "Server error"
        return jsonify(message)
    message['success'] = True
    message['message'] = "Posted message"
    return jsonify(message)

if __name__ == '__main__':
    database_helper.init_db()
    app.debug = True
    app.run()
