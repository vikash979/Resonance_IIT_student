from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import (
    login, logout
)
from learner.custom_functions import authenticate
from identity_service.models import StudentInfo
from rest_framework import HTTP_HEADER_ENCODING
from subjects.models import HasSubjects
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as gl
from learner.serilaizer import (
    StudentProfileSerializer, HasSubjectsSerializer
)

def get_token_from_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)
        if auth:
            _, token = auth.split()
            return token.decode()
        msg = gl('Invalid token header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    msg = gl('Invalid token header. No credentials provided.')
    raise exceptions.AuthenticationFailed(msg)

class LearnerLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    def post(self, request, *args, **kwargs):
        username_var = self.request.data.get('username', None)
        password_var = self.request.data.get('password', None)
        if username_var and password_var is not None:
            check_user = authenticate(user=username_var, passwd=password_var)
            if check_user is not None:
                get_token, _ = Token.objects.get_or_create(user=check_user)
                login(self.request, check_user)
                data = Response({'data': {'ur_t': get_token.key}, 'error': [], 'status': True})
                data.set_cookie('ur_t', get_token.key)
                return data
            return Response({'data': [], 'error': 'Please provide correct username or password', 'status': False})
        return Response({'data': [], 'error': 'Please provide correct username or password', 'status': False})

class LearnerLogoutAPIView(APIView):
    def get_model(self):
        from rest_framework.authtoken.models import Token
        return Token

    def post(self, request, *args, **kwargs):
        response = Response({"data": [], 'error': [], 'status': True})
        key = get_token_from_header(self.request)
        if key:
            self.get_model().objects.get(key=key).delete()
            response.delete_cookie('ur_t')
            return response
        return Response({"data": [], 'error': [], 'status': True})

class LearnerProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        get_token = get_token_from_header(self.request)
        get_user = Token.objects.get(key=get_token).user
        get_learner_user = StudentInfo.objects.get(user_id=get_user.id)
        serilaizer_var = StudentProfileSerializer(get_learner_user)
        return Response({'data': serilaizer_var.data, 'error': [], 'status': True})

class LearnerDashboardAPIView(APIView):
    def post(self, request, *args, **kwargs):
        get_token = get_token_from_header(self.request)
        get_user = Token.objects.get(key=get_token).user
        get_learner_user = StudentInfo.objects.get(user_id=get_user.id)
        user_subjects = HasSubjects.objects.filter(class_id = get_learner_user.student_class)
        serializer_var = HasSubjectsSerializer(user_subjects, many=True)
        return Response({'data': serializer_var.data, 'error': [], 'status': True})
