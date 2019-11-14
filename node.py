from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from medscheme import *

app = Flask(__name__)
CORS(app)

preprocess()

@app.route('/get-disease', methods=['POST'])
def get_disease():
    engine = FindMyDisease()
    
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
        get_patient_symptoms(pat_symptoms)
        
        engine.reset()
        engine.run()
        if disease_definition != None: 
            response = {
                'message' : 'success',
                'name': disease_definition['name'],
                'description': disease_definition['description'],  
                'treatment': disease_definition['treatment']
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
        engine.reset()  

@app.route('/get-other-diseases', methods=['POST'])
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
        get_patient_symptoms(pat_symptoms)
        alternate_diseases = FindAltDisease.identify_alt_disease()
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
        pass
    
@app.route('/diseases/<disease>', methods=['GET'])
def get_specific_disease(disease):
    if disease == '' or disease == None:
        response = {
            'message': 'Disease not found'
        }
        return jsonify(response), 400   
    
      
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3000)
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)