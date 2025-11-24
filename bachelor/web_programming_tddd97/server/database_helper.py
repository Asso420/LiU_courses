import sqlite3
from flask import g

DATABASE = './database.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE)
    return db

def disconnect():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None


def init_db():
    with open("schema.sql", "r") as file:
        content = file.read()
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.executescript(content)
    db.commit()
    db.close()

def validate_token(token):
    cursor = get_db().execute("select email, token from tw_logged_in where token =?;", [ token])
    match = cursor.fetchone()
    cursor.close()
    if match is None:
        return None
    ret = {'email': match[0], 'token': match[1]}
    return ret

def delete_token(email):
    try:
        cursor = get_db().execute("delete from tw_logged_in where email =?;", [ email])
        get_db().commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False
'''
CREATE TABLE tw_logged_in (
    email VARCHAR(50) NOT NULL,
    token VARCHAR(36),
    CONSTRAINT pk_tw_logged_in PRIMARY KEY(email),
    CONSTRAINT fk_logged_user FOREIGN KEY (email) REFERENCES tw_users(email) ON DELETE SET NULL
);
'''
def add_logged_in(email, token):
    try:
        get_db().execute("INSERT INTO tw_logged_in VALUES(?,?)", [email, token])
        get_db().commit()
        return True
    except Exception as e:
        print(e)
        return False

def create_user(fname, lname, email, country, city, gender, password):
    try:
        get_db().execute("INSERT INTO tw_users VALUES(?,?,?,?,?,?,?);", [fname, lname, email, country, city, gender, password])
        get_db().commit()
        return True
    except Exception as e:
        print(e)
        return False
'''
CREATE TABLE tw_users (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    password VARCHAR(50) NOT NULL,
    CONSTRAINT pk_tw_users PRIMARY KEY(email)
);
'''
def valid_password(email, password):
    cursor = get_db().execute("select email from tw_users where email = ? and password =?;", [ email, password])
    match = cursor.fetchone()
    cursor.close()
    if match is None:
        return False
    return True

def set_password(email, password):
    try:
        cursor = get_db().execute("UPDATE tw_users SET password = ? WHERE email = ?;", [password, email])
        get_db().commit()
        if cursor.rowcount == 0:
            return False
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_user(email):
    cursor = get_db().execute("select fname, lname, email, country, city, gender from tw_users where email = ?;", [ email])
    match = cursor.fetchone()
    cursor.close()
    match_types = ['firstname', 'familyname','email','country','city','gender']
    if match is None:
        return None
    match_types = ['firstname', 'familyname', 'email', 'country', 'city', 'gender']
    user_data = {match_types[i]: match[i] for i in range(len(match_types))}
    return user_data


def remove_user(email):
    pass


'''
 CREATE TABLE tw_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id VARCHAR(50) NOT NULL,
    to_id VARCHAR(50) NOT NULL,
    msg VARCHAR(128) NOT NULL,
    CONSTRAINT fk_from_messages FOREIGN KEY (from_id) REFERENCES tw_users(email),
    CONSTRAINT fk_to_messages FOREIGN KEY (to_id) REFERENCES tw_users(email)
);
'''


def create_post(from_email, to_email, msg):
    try:
        get_db().execute("INSERT INTO tw_messages (from_id, to_id, msg) VALUES(?,?,?)", [from_email, to_email, msg])
        get_db().commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_posts(email):
    cursor = get_db().execute("select from_id, msg from tw_messages where to_id = ?;", [ email])
    matches = cursor.fetchall()
    cursor.close()
    if matches is None:
        return None
    return matches

