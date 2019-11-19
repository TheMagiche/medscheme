from difflib import SequenceMatcher
from experta import *
from collections import OrderedDict


import json


diseases_list = []

symptom_map = {}

d_desc_map = {}

d_treatment_map = {}

patients_symptoms = [] 


def preprocess():
    global diseases_list,symptom_map,d_desc_map,d_treatment_map
    
    try:
        with open("diseases.txt", mode='r') as f:
            diseases_list = f.read().split("\n")
            # print(diseases_list)

    except (IOError, IndexError):
        pass
    finally:
        print("Successfully acquired diseases")

    
    try:
        for disease in diseases_list:
            with open("Description/"+ disease + ".txt", mode='r') as f:
                d_desc_map[disease] = f.read()
                # print(d_desc_map)

            with open("Symptoms/"+ disease + ".txt", mode='r') as f:
                symptom_map[disease] = f.read().split("\n")
               

            with open("Treatment/"+ disease + ".txt", mode='r') as f:
                d_treatment_map[disease] = f.read()
                # print(d_treatment_map)
        # print(symptom_map)

    except (IOError, IndexError):
        print("Failed")
    finally:
        print("Successfully acquired descriptions, symptoms, treatment")    
        

def get_patient_symptoms(sym=[]):
    global patients_symptoms
    
    for s in sym:
        patients_symptoms.append(s)   
    
    return patients_symptoms 
        
        
def get_details(disease):
	return d_desc_map[disease]


def get_treatments(disease):
	return d_treatment_map[disease]


def get_disease_symptoms(disease):  
    return symptom_map[disease]
    
    
def return_specific_disease(disease):    
    specific_disease_definition = OrderedDict([('name',disease),('description',get_details(disease)), ('treatment', get_details(disease))])
    return specific_disease_definition     


def get_all_diseases():
    return diseases_list


preprocess()

class Symptom(Fact):
    symptom = Field(list, mandatory=True)
    
    
class Disease():
    def __init__(self):
        self.pat_symptoms = patients_symptoms
        self.disease_definition = OrderedDict()
    
    
class FindAltDisease():
    @staticmethod
    def identify_alt_disease(pat_sym=[]):
        probable_diseases_list = []
        symptom_list = []      
        
        for symptom in pat_sym:
            symptom_list.append(symptom)

        # print("Symptom list: ", symptom_list)
      
        for disease in diseases_list:
            # print(disease ,"symptoms: ",symptom_map[disease])
            ratio = SequenceMatcher('',symptom_map[disease], symptom_list).ratio()
            if(ratio > 0.4):
                probable_diseases_list.append(disease)
      
        print("You may also have: ",probable_diseases_list) 

        return probable_diseases_list
 
 
class FindMyDisease(KnowledgeEngine, Disease):
        
    def return_disease(self, disease):
        self.disease_definition = OrderedDict([('name',disease),('description',get_details(disease)), ('treatment', get_details(disease))])
        return self.disease_definition 
    
    def no_disease(self):
        self.disease_definition = OrderedDict([('name',"Unknown"),('description',"Can't find disease"), ('treatment', "Unknown")])
        return self.disease_definition 
    
    @Rule()
    def startup(self):
        print("Welcome to medscheme")
        print("Lets see what ails you")
        self.declare(Symptom(symptom=patients_symptoms))
           
         
    @Rule(Symptom(symptom= get_disease_symptoms('Alzheimers')))
    def declare_alzheimers(self):
        print('You have alzheimer')
        self.return_disease("Alzheimers")
        
     
    @Rule(Symptom(symptom= get_disease_symptoms('Arthritis')))
    def declare_arthritis(self):
        print('You have arthritis')
        self.return_disease("Arthritis")
        
        
    
    @Rule(Symptom(symptom= get_disease_symptoms('Asthma')))
    def declare_asthma(self):
        print('You have asthma')
        self.return_disease("Asthma")
        
    
    @Rule(Symptom(symptom= get_disease_symptoms('Diabetes')))
    def declare_diabetes(self):
        print('You have diabetes')
        self.return_disease("Diabetes")
        
    
    @Rule(Symptom(symptom= get_disease_symptoms('Epilepsy')))
    def declare_epilepsy(self):
        print('You have epilepsy')
        self.return_disease("Epilepsy")
        
 
    @Rule(Symptom(symptom= get_disease_symptoms('Glaucoma')))
    def declare_glaucoma(self):
        print('You have glaucoma')
        self.return_disease("Glaucoma")
        
        
    @Rule(Symptom(symptom= get_disease_symptoms('Heart Disease')))
    def declare_heart_disease(self):
        print('You have Heart Disease')
        self.return_disease("Heart Disease")
       
    
    @Rule(Symptom(symptom= get_disease_symptoms('Heat Stroke')))
    def declare_heat_stroke(self):
        print('You have Heat Stroke')
        self.return_disease("Heat Stroke")
        

    @Rule(Symptom(symptom= get_disease_symptoms('Hyperthyroidism')))
    def declare_hyperthyroidism(self):
        print('You have hyperthyroidism')
        self.return_disease("Hyperthyroidism")
        
    
    @Rule(Symptom(symptom= get_disease_symptoms('Hypothermia')))
    def declare_hypothermia(self):
        print('You have Hypothermia')
        self.return_disease("Hypothermia")
        
    
    @Rule(Symptom(symptom= get_disease_symptoms('Jaundice')))
    def declare_jaundice(self):
        print('You have jaundice')
        self.return_disease("Jaundice")
       
    
    @Rule(Symptom(symptom= get_disease_symptoms('Sinusitis')))
    def declare_sinusitis(self):
        print('You have sinusitis')
        self.return_disease("Sinusitis")
        
    
    @Rule(Symptom(symptom=get_disease_symptoms('Tuberculosis')))
    def declare_tuberculosis(self):
        print('You have Tuberculosis')
        self.return_disease("Tuberculosis")
       
    @Rule(NOT(Symptom(symptom=get_disease_symptoms('Alzheimers'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Alzheimers'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Arthritis'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Asthma'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Diabetes'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Epilepsy'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Glaucoma'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Heart Disease'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Heat Stroke'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Hyperthyroidism'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Hypothermia'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Jaundice'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Sinusitis'))) |
        NOT(Symptom(symptom=get_disease_symptoms('Tuberculosis')))
        )
    def declare_no_disease(self):
        self.no_disease()


