from flask import Flask, jsonify, request
from people import PeopleAPI
from database import Database
from exceptions import ParanuaraException, InvalidCompanyNameException, IncorrectParametersException


app = Flask(__name__)
port = 5000

@app.route('/')
def index():
    return jsonify({'message': "Hello welcome to the world of paranuara. Totally not our password btw."})

@app.route('/paranuara/api/v1.0/people/company_name/<string:company_name>')
def get_employees(company_name):
    try:
        paranuaradb = Database.get_db_conn()
        rows = PeopleAPI.get_employees_of_company(paranuaradb, company_name)
        return jsonify(rows)
    except ParanuaraException as e:
        print('caught exception e')
        return str(e), e.HttpErrorCode

@app.route('/paranuara/api/v1.0/people/mutual_living_browneyed_friends/')
def get_mutual_living_browneyed_friends():
    try:
        person1_index  = request.args.get('person1_index', None)
        person2_index  = request.args.get('person2_index', None)
        if person1_index is None or person2_index is None:
            raise IncorrectParametersException('Indices for 2 people not supplied') 


        paranuaradb = Database.get_db_conn()
        rows = PeopleAPI.get_mutual_friends_with_brown_eyes_alive(paranuaradb, person1_index, person2_index)
        return jsonify(rows)
    except ParanuaraException as e: 
        return str(e), e.HttpErrorCode

@app.route('/paranuara/api/v1.0/people/get_fruits_and_veggies/<string:person_id>')
def get_fruits_and_veggies(person_id):
    try:
        paranuaradb = Database.get_db_conn()
        rows = PeopleAPI.get_fruits_and_veggies(paranuaradb, person_id)
        return jsonify(rows)
    except ParanuaraException as e:
        return str(e), e.HttpErrorCode

if __name__ == '__main__':
    app.run(debug=True, port=port)