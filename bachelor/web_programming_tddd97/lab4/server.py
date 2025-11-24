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
from apscheduler.schedulers.background import BackgroundScheduler


alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" # Used for token generation

active_connections = {} # An empty dictionary to store the active connections

users_online_timeline = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # A list to store the number of users online in the last 20 minutes
users_online = 0

last_update_time = datetime.now() # The time of the last update of the users_online_timeline
def update_users_online_timeline(): # A function to update the users_online_timeline
    global users_online
    global users_online_timeline
    global last_update_time
    users_online_timeline[19] = users_online
    if datetime.now() - last_update_time >= timedelta(minutes=1): # If the last update was more than a minute ago
        users_online_timeline.pop(0) # Remove the first element
        users_online_timeline.append(users_online)  # Add the current number of users online to the end
        last_update_time = datetime.now()   # Update the last update time
    for user_email, conn in active_connections.items(): # For each active connection

        try:
            ret = {} # Create a dictionary to store the message
            ret['action'] = 'update_timeline' # Set the action to update_timeline
            ret['data'] = users_online_timeline # Set the data to the users_online_timeline
            conn['ws'].send(json.dumps(ret)) # Send the message to the client
        except Exception as e:
            print(f"Error sending message to {user_email}: {e}")



scheduler = BackgroundScheduler() # Create a scheduler
scheduler.add_job(update_users_online_timeline, 'interval', seconds=5) # Add the update_users_online_timeline function to the scheduler
scheduler.start() # Start the scheduler

def update_gender_distribution(): # A function to update the gender distribution
    gender_data = database_helper.get_gender_distribution() # recieves the gender distribution from the database
    for user_email, conn in active_connections.items(): # For each active connection
        try:
            conn['ws'].send(json.dumps({'action': 'update_chart', 'data': gender_data})) # Send the gender distribution to the client via ws
        except Exception as e:
            print(f"Error sending gender update to {user_email}: {e}")
scheduler.add_job(update_gender_distribution, 'interval', seconds=5) # updating the chart every 5 seconds



app = Flask(__name__) # Create a Flask app
sock = Sock(app) # Create a Flask-Sock app
bcrypt = Bcrypt(app) # Create a Bcrypt app
 
@app.teardown_request # A function to disconnect from the database after each request
def teardown(exception): # The function to disconnect from the database
    database_helper.disconnect() # Disconnect from the database

######################## Static Files #####################################

@app.route("/", methods=['GET']) # A route to serve the client.html file
def get_index(): # The function to serve the client.html file
    return current_app.send_static_file('client.html')

@app.route("/<file>", methods=['GET']) # A route to serve the static files
def get_index_js(file):
    return current_app.send_static_file(file) # Serve the static files


############################################################################






@sock.route("/connect") # A route to connect to the websocket
def connect(ws): # The function to connect to the websocket
    global users_online
    token = request.args.get('token') # Get the token from the request
    etok = database_helper.validate_token(token) # Validate the token
    if etok == None:
        ws.close()
        return
    active_connections[etok['email']] = { # Add the connection to the active_connections dictionary
        "ws": ws,
        "token": etok['token']
    }
    
    users_online = users_online +1 # Increment the number of users online
    try: 
        while True: # While the connection is open
            message = ws.receive() # Receive a message
            if message is None:
                break
            try:
                data = json.loads(message) # Parse the message as JSON
            except json.JSONDecodeError:
                print("Received invalid JSON")
                continue
    except Exception as e:
        print("Exception error:", e)
    finally:
        conn = active_connections.get(etok['email']) # Get the connection from the active_connections dictionary
        users_online = users_online - 1 # Decrement the number of users online
        if conn is not None and conn.get('token') == etok['token']:
            conn['ws'].close()
            active_connections.pop(etok['email'], None) # Remove the connection from the active_connections dictionary






    

def valid_email(email): # A function to validate an email
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

@app.route("/sign_up", methods=['POST']) 
def sign_up(): # A function to sign up a user
    data = request.get_json() # Get the JSON data from the request
    message = {}
    message['success'] = False
    if data is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if not data['email'] or  not data['password'] or  not data['firstname'] or  not data['familyname'] or  not data['gender'] or  not data['city'] or not data['country']:
        message['message'] = "Wrong form"
        return jsonify(message), 400
    if not valid_email(data['email']):  # Check if the email is valid
        message['message'] = "Not a valid email"
        return jsonify(message), 400
    if len(data['password']) < 5:  # Check if the password is at least 5 characters long
        message['message'] = "Password too short"
        return jsonify(message), 400
    if database_helper.get_user(data['email']) != None:  
        message['message'] = "User already exsist"
        return jsonify(message), 409
    pw_hash = bcrypt.generate_password_hash(data['email'] + data['password']).decode('utf-8') # Generate a password hash
    if not database_helper.create_user(data['firstname'], data['familyname'], data['email'], data['country'], data['city'], data['gender'], pw_hash):   # Create the user in the database
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Created user sucessfully"
    return jsonify(message), 201

def generate_token(): # A function to generate a random token
    token = ""
    for i in range(36):
        token += alph[random.randint(0, len(alph)-1)] # Add a random character from the alphabet to the token
    return token

@app.route("/sign_in", methods=['POST']) # A route to sign in a user
def sign_in():
    global users_online
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
    
    hashed_pw = database_helper.get_password(data['username']) # Get the hashed password from the database
    if hashed_pw == None:
        message['message'] = "invalid email or password"
        return jsonify(message), 401
    if bcrypt.check_password_hash(hashed_pw, data['username'] + data['password']) == False:
        message['message'] = "invalid email or password"
        return jsonify(message), 401
    token = generate_token() # Generate a token
    database_helper.delete_token(data['username']) # Delete the old token
    conn = active_connections.get(data['username']) # Get the connection from the active_connections dictionary
    if conn is not None: # If the connection exists
        try:
            ret = {}
            ret['action'] = 'sign_out' # Set the action to sign_out
            conn['ws'].send(json.dumps(ret)) # Send the message to the client
            conn['ws'].close() # Close the connection
        except:
            pass
        active_connections.pop(data['username'], None) # Remove the connection from the active_connections dictionary
    if database_helper.add_logged_in(data['username'],token) == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    


    message['success'] = True
    message['message'] = "Login success"
    message['data'] = token
    return jsonify(message), 200

@app.route("/sign_out", methods=['DELETE'])
def sign_out(): # A function to sign out a user
    global users_online
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization') # Get the Authorization header from the request
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not database_helper.delete_token(etok['email']): # Delete the token from the database 
        message['message'] = "Server error"
        return jsonify(message), 500
    conn = active_connections.get(etok['email']) # Get the connection from the active_connections dictionary
    if conn is not None: # If the connection doea not exist
        try:
            ret = {}
            ret['action'] = 'sign_out' # Set the action to sign_out
            conn['ws'].send(json.dumps(ret)) # Send the message to the client
            conn['ws'].close() # Close the connection
        except:
            pass
        active_connections.pop(etok['email'], None) # Remove the connection from the active_connections dictionary
    
    message['success'] = True
    message['message'] = "sucessfully logged out"
    return jsonify(message), 200

@app.route("/change_password", methods=['PUT'])
def change_password(): # A function to change the password of a user
    data = request.get_json()   # Get the JSON data from the request
    
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    
    if data is None or 'data' not in data or data['data'] is None: # Check if the data is valid
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
    json_message = json.dumps(data['data'], separators=(',', ':')) # Create a JSON string of the message
    msg_hash = hmac.new(token.encode('utf-8'), json_message.encode('utf-8'), hashlib.sha256).hexdigest()    # Create a hash of the message

    if msg_hash != data['hash']:    # Check if the hash of the message is correct
        message['message'] = "Invalid message 123"
        return jsonify(message), 401

    hashed_pw = database_helper.get_password(etok['email']) # Get the hashed password from the database
    if hashed_pw is None:
        message['message'] = "Invalid email or password"
        return jsonify(message), 401

    if not bcrypt.check_password_hash(hashed_pw, etok['email'] + data['data']['oldpassword']): # Check if the old password is correct
        message['message'] = "Invalid email or password"
        return jsonify(message), 401

    pw_hash = bcrypt.generate_password_hash(etok['email'] + data['data']['newpassword']).decode('utf-8') # Generate a new password hash with the new password

    if not database_helper.set_password(etok['email'], pw_hash):    # Set the new password in the database
        message['message'] = "Server error"
        return jsonify(message), 500

    message['success'] = True
    message['message'] = "Changed password"
    return jsonify(message), 200


@app.route("/get_user_data_by_token", methods=['GET'])
def get_user_data_by_token(): # A function to get the user data by token
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization') # Get the Authorization header from the request
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
def get_user_data_by_email(email): # A function to get the user data by email
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
def get_user_messages_by_token():  # A function to get the messages of a user by token
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
    ret = database_helper.get_posts(etok['email']) # Get the messages of the user from the database
    if ret is not None and ret == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/get_user_messages_by_email/<email>", methods=['GET'])
def get_user_messages_by_email(email): # A function to get the messages of a user by email
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not valid_email(email):
        message['message'] = "Invalid email"
        return jsonify(message), 404
    etok = database_helper.validate_token(auth_header) # Validate the token from the Authorization header
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if database_helper.get_user(email) == None: # Check if the user exists in the database
        message['message'] = "User does not exist"
        return jsonify(message), 404
    ret = database_helper.get_posts(email) # Get the messages of the user from the database
    if ret is not None and ret == False:
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True
    message['message'] = "Messages retrieved"
    message['data'] = ret
    return jsonify(message), 200

@app.route("/post_message", methods=['POST'])
def post_message(): # A function to post a message to a user
    data = request.get_json()
    message = {}
    message['success'] = False
    auth_header = request.headers.get('Authorization')
    if data is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if data['data'] is None:
        message['message'] = "No data"
        return jsonify(message), 400
    if auth_header == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not data['data']['email'] or not data['data']['message']:
        message['message'] = "Missing data"
        return jsonify(message), 400
    if data['data']['message'] == "":
        message['message'] = "No message"
        return jsonify(message), 400
    etok = database_helper.validate_token(auth_header)
    if etok == None:
        message['message'] = "Not logged in"
        return jsonify(message), 401
    if not valid_email(data['data']['email']):
        message['message'] = "Invalid email"
        return jsonify(message), 400
    if database_helper.get_user(data['data']['email']) == None:
        message['message'] = "User does not exist"
        return jsonify(message), 400
    
    timestamp = datetime.fromisoformat(data['data']['time'].replace("Z", "+00:00")).replace(tzinfo=timezone.utc) # Get the timestamp from the data 
    current_time = datetime.now(timezone.utc) # Get the current time

    if current_time - timestamp > timedelta(minutes=1): # Check if the message is older than 1 minute
        message['message'] = "Old message"
        return jsonify(message), 401

    token = etok['token']
    json_message = json.dumps(data['data'], separators=(',', ':')) # Create a JSON string of the message
    msg_hash = hmac.new(token.encode('utf-8'), json_message.encode('utf-8'), hashlib.sha256).hexdigest() # Create a hash of the message 

    if msg_hash != data['hash']:    # Check if the hash of the message is correct
        message['message'] = "Invalid message"
        return jsonify(message), 401

    if not database_helper.create_post(etok['email'], data['data']['email'], data['data']['message']): # Create the message in the database
        message['message'] = "Server error"
        return jsonify(message), 500
    message['success'] = True # Set the success to True
    message['message'] = "Posted message" # Set the message to "Posted message"
    return jsonify(message), 201

if __name__ == '__main__': # If the script is run directly
    database_helper.init_db()   # Initialize the database
    app.debug = True    # Set the app to debug mode
    app.run()   # Run the app
