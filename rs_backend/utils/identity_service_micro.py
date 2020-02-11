import requests
from django.conf import settings
import json

def identity_to_has_subject(id):
    conditions = {}
    conditions["id"]=id
    # paginations = {}
    # paginations["page"] = 0
    data = {}
    data["action"]="view"
    data["conditions"]=json.dumps(conditions)
    # data["paginations"] =json.dumps(paginations)
    url = settings.IDENTITY_SERIVICE_MICROSERVICE_CLASS
    subject_request = requests.post(url, data=data)
    return json.loads(subject_request.text)["data"]
    