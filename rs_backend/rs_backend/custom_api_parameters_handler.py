from django.apps import apps
from django.urls import resolve

class ApiParameterHandler:
    def __init__(self, request=None, app_label_name=None, *args, **kwargs):
        if request and app_label_name:
            self.data = request.data

    def post(self, request, *args, **kwargs):
        pass
