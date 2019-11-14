from uuid import uuid4

class PatientInfo():
    
    def __init__(self, id , name, age , marital_status):
        self.id = None
        self.name = None
        self.age = None
        self.marital_status = None
        
    def get_id(self):
        self.id = str(uuid4())
    def send_id(self):
        return self.id
    
    def get_name(self, name):
        self.name = name
    def send_name(self):
        return name
    
    def get_age(self, age):
        self.age = age
    def send_age(self):
        return self.age    
    
    def get_m_status(self, m_status):
        self.marital_status = m_status
    def send_m_status(self):
        return self.martial_status
    
    
class PatientDiagnosis():
    def __init__(self, *args):
        self.symptoms = args  
    
    def send_symptoms(self):
        return self.symptoms
    
   