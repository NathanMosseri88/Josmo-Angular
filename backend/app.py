from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'nathanm'
# app.config['MYSQL_PASSWORD'] = 'Simple123'
# app.config['MYSQL_DB'] = 'josmo'
# mysql = MySQL(app)

@app.route('/api/login', methods=['POST'])
def login(): 
    login_data = request.get_json()
    print(login_data)
    return login_data

@app.route('/api/presets', methods=['GET', 'POST'])
def create_preset():
    if request.method == 'GET':
        return ['ex1 - from API', 'ex2', 'ex3']
    elif request.method == 'POST':
        preset_data = request.get_json()
        print(preset_data)
        return preset_data

@app.route('/api/proposals', methods=['POST'])
def createProposal(): 
    proposal_data = request.get_json()
    print(proposal_data)
    return proposal_data

if __name__ == '__main__': 
    app.run(debug=True)