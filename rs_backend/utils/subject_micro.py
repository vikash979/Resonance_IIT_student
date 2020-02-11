import requests
from django.conf import settings
import json

def subject_to_class(id):
    conditions = {}
    conditions["id"]=id
    # paginations = {}
    # paginations["page"] = 0
    data = {}
    data["action"]="view"
    data["conditions"]=json.dumps(conditions)
    # data["paginations"] =json.dumps(paginations)
    url = settings.INSTITUTE_MICROSERVICE_CLASS
    subject_request = requests.post(url, data=data)
    return json.loads(subject_request.text)["data"]
    