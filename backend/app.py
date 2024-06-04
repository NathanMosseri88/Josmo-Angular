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

@app.route('/api/presets', methods=['POST'])
def create_preset():
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