from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from medscheme import *
from functools import wraps
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app
from config import Config
from flask_migrate import Migrate
import jwt

from models import db, User



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/api/login/', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user.email,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('UTF-8') })

@app.route('/api/register/', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/api/get-disease', methods=['POST'])
def get_disease():
    preprocess()   
    values = request.get_json()
    if not values:
        response = {
            'message': 'Enter correct values'
        }
        return jsonify(response), 404
    
    required_fields = ['patients_symptoms']
    
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400
    
    pat_symptoms = values['patients_symptoms']
    get_patient_symptoms(pat_symptoms)
    
    try:
        engine.run()
        if engine.disease_definition != None: 
            response = {
                'message' : 'success',
                'name': engine.disease_definition['name'],
                'description': engine.disease_definition['description'],  
                'treatment': engine.disease_definition['treatment']
            }
            
            return jsonify(response), 201
        else: 
            response = {
                'message':'Your symptoms did not match any disease on our database.'
            }
           
            return jsonify(response),  500
    except():
        response = {
            'message':'failed'
        }
        
        return jsonify(response),  500
    finally:
        print("reseting engine...")
        engine.reset()
        print("Done")
        engine.run()

@app.route('/api/get-other-diseases', methods=['POST'])
def get_alt_disease():
    
    values = request.get_json()
    
    if not values:
        response = {
            'message': 'Enter correct values'
        }
        return jsonify(response), 404
    
    required_fields = ['patients_symptoms']
    
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400
    
    pat_symptoms = values['patients_symptoms']
       
    try:
        alternate_diseases = FindAltDisease.identify_alt_disease(pat_symptoms)
        if alternate_diseases != None: 
            response = {
                'message' : 'success',
                'alt_diseases': alternate_diseases
            }
            return jsonify(response), 201
        else: 
            response = {
                'message':'failed'
            }
            return jsonify(response),  500
    except():
        response = {
            'message':'failed'
        }
        return jsonify(response),  500
    finally:
        print("Done")

@app.route('/api/diseases', methods=['GET'])
def get_all_disease():
    mydisease_list = get_all_diseases()    
    response = {
        'message': 'Success',
        'disease_list': mydisease_list
    }
    return jsonify(response), 200
    
@app.route('/api/diseases/<disease>', methods=['GET'])
def get_specific_disease(disease):
    if disease == '' or disease == None:
        response = {
            'message': 'Disease not found'
        }
        return jsonify(response), 400   
    disease_def = return_specific_disease(disease)
    if disease_def != None: 
        response = {
            'message' : 'success',
            'name': disease_def['name'],
            'description': disease_def['description'],  
            'treatment': disease_def['treatment']
        }
        return jsonify(response),  200  
    else: 
        response = {
            'message': 'Disease not found'
        }
        return jsonify(response), 400 

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify



if __name__ == '__main__':
    preprocess()
    engine = FindMyDisease()
    engine.reset()
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3000)
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)

