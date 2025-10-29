import os
import sqlite3
import json
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

#SQL Alchemy attempt
#db = SQLAlchemy()
#DB_NAME = "database.db"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
#SQL Alchemy attempt
#app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')


def get_input_keys(json_path=None):
    """
    Read `public/inputs.json` and return a list of top-level keys.

    If `json_path` is not provided, the function will look for `public/inputs.json`
    next to this file. Keys are stripped of leading/trailing whitespace.

    Returns an empty list if the file is missing or the JSON root is not an object.
    """
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), 'public', 'inputs.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # malformed JSON
        return []

    if isinstance(data, dict):
        # strip whitespace from keys and preserve order
        return [k.strip() for k in data.keys()]
    return []
#SQL Alchemy attempt
#db.init_app(app)


#This function creates a database if the database doesn't exist
def create_database(app):
    print("Entered into function")
    if not path.exists('BEST Scoring Webpage/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database created!")

#SQL Alchemy attempt
#create_database(app)









# API endpoint to validate localStorage and create session
@app.route('/api/validate-session', methods=['POST'])
def validate_session():
    """Client sends code and match# from localStorage; server creates session"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    code = data.get('code')
    match_num = data.get('matchNum')
    
    if not code or not match_num:
        return jsonify({'error': 'Missing code or match number'}), 400
    
    # Store in server session
    session['authenticated'] = True
    session['code'] = code
    session['match_num'] = match_num
    
    return jsonify({'status': 'success', 'message': 'Session created'}), 200

# CALEB BUILD HERE
@app.route('/api/data', methods=['POST'])
def recv_data():
    """Existing data endpoint"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    #Do things with data
    #print(data)
    #print(data.keys())
    storeJSONInDatabase(data)
    
    
    response = {
        'status': 'sucesss',
        'message': 'Data saved to database'
    }
    return jsonify(response), 200


def storeJSONInDatabase(json):
    #Read the keys and values and turn them into SQL commands
    #Remove all the spaces in each key, so the
    keys = ["Z" + key.replace(" ", "_").replace("-", "_") for key in json]
    keyStr = ", ".join(keys)
    keyStr = "(match_id, " + keyStr + ")"

    keysTypes = " TEXT, ".join(keys)
    keysTypes = "(match_id INTEGER, " + keysTypes + " TEXT)"

    id = str(json["matchNum"])
    values = json.values()
    valuesStr = '","'.join(values)
    valuesStr = '("' + id + '","' + valuesStr + '")'

    sql = "CREATE TABLE IF NOT EXISTS scoress " + keysTypes
    sql2 = "INSERT INTO scoress " + keyStr + " VALUES " + valuesStr

    #Execute SQL commands
    connection = sqlite3.connect("scores.db", timeout=10)
    cursor = connection.cursor()
    print(sql)
    print(sql2)
    # cursor.execute(sql)
    # cursor.execute(sql2)
    connection.commit()
    cursor.close()
    connection.close()

# def storeJSONInDatabase(json):
#     connection = sqlite3.connect("scores.db", timeout=10)
#     cursor = connection.cursor()
#     keys = ["Z" + key.replace(" ", "_").replace("-", "_") for key in json]
#     keyStr = ", ".join(keys)
#     # keyStr = "(match_id, " + keyStr + ")"

    

@app.route('/')
def index():
    """Serve sign-in page at root"""
    return send_from_directory(PUBLIC_DIR, 'sign-in.html')


@app.route('/scoreboard.html')
def scoreboard():
    """Protected route - only accessible after sign-in"""
    if not session.get('authenticated'):
        # Redirect to sign-in if not authenticated
        return redirect(url_for('index'))
    return send_from_directory(PUBLIC_DIR, 'scoreboard.html')


@app.route('/<path:filename>')
def serve_public_files(filename):
    """Serve other static files (CSS, JS, images, etc.)"""
    # Prevent direct access to scoreboard.html through this route
    if filename == 'scoreboard.html':
        return redirect(url_for('scoreboard'))
    
    try:
        return send_from_directory(PUBLIC_DIR, filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


def resetDatabase():
    connection = sqlite3.connect("scores.db", timeout=10)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS scoress")
    connection.commit()
    cursor.close()
    connection.close()
    print("###DATABASE SUCESSFULLY RESET###")

if __name__ == '__main__':
    # Use 0.0.0.0 so the server is reachable from other hosts if needed
    # Debug off by default; can set FLASK_DEBUG=1 env var when developing
    #if(input("Reset database? (y/n): ") == "y"):
    #    resetDatabase()
    app.run(host='0.0.0.0', port=5000)





    
