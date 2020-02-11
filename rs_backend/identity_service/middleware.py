# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
#
# class AuthenticationObjectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.path == "/auth/api/login/" and request.method == "POST":
#             serializer = AuthTokenSerializer(data=request.POST, context={'request': request})
#             serializer.is_valid(raise_exception=True)
#             user = serializer.validated_data['user']
#             token = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
