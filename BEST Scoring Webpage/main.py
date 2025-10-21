import os
import sqlite3
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

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

    #Read the keys and values and turn them into SQL commands
    #Remove all the spaces in each key, so the
    keys = ["Z" + key.replace(" ", "_").replace("-", "_") for key in data]
    keyStr = ", ".join(keys)
    keyStr = "(match_id, " + keyStr + ")"

    keysTypes = " TEXT, ".join(keys)
    keysTypes = "(match_id INTEGER, " + keysTypes + " TEXT)"

    id = str(data["matchNum"])
    values = data.values()
    valuesStr = '","'.join(values)
    valuesStr = '("' + id + '","' + valuesStr + '")'

    sql = "CREATE TABLE IF NOT EXISTS scoress " + keysTypes
    sql2 = "INSERT INTO scoress " + keyStr + " VALUES " + valuesStr

    #Execute SQL commands
    connection = sqlite3.connect("scores.db", timeout=10)
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.execute(sql2)
    connection.commit()
    cursor.close()
    connection.close()
    
    response = {
        'status': 'sucesss',
        'message': 'Data saved to database'
    }
    return jsonify(response), 200


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
    if(input("Reset database? (y/n): ") == "y"):
        resetDatabase()
    app.run(host='0.0.0.0', port=5020)





    
