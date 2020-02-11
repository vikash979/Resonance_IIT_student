# from django.shortcuts import render
# from django.contrib.auth.models import User
from json import loads, dumps
from datetime import datetime
from .custom_functions import get_action, pagination_function
from rs_backend.custom_api_parameters_handler import ApiParameterHandler
from django.contrib.auth import (
    login, authenticate, logout
)
from rest_framework import status
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.generics import (
    ListAPIView
)
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny
)
from .custom_permissions import (
    UserCreatePermission, UserListPermissionReadOnly
)
from identity_service.serializers import (
    UsersModelSerializer, CountrySerializer, RegionSerializer,
    StateSerializer, CitySerializer, CenterSerializer,
    DesignationSerializer, EmploymentTypeSerializer, DepartmentSerializer,
    ConceptSerializer, UserConceptSerializer, DivisionSerializer,
    SkillSerializer, FacultiesSerializer, DepartmentMappingSerializer,
    StudentInfoSerializer, StudentInfoSerializerOnly
)
from identity_service.models import (
    User, Country, Region, State, City, Center, Designation,
    EmploymentType, Departments, Concept, UserConcepts,
    Faculties, Facultyhassubjects, Division, Skill, UserBatch,
    DepartmentMapping, DesignationMapping, EmploymentTypeMapping,
    StudentInfo, StudentHasSubjects
)

app_label = 'identity_service'

class DemoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return ApiParameterHandler(request=self.request, app_label_name=app_label)

class UserAuthenticationAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    def post(self, request, *args, **kwargs):
        username_var = self.request.data.get('username', None)
        password_var = self.request.data.get('password', None)
        if username_var and password_var is not None:
            check_user = authenticate(username=username_var, password=password_var)
            if check_user is not None:
                get_token, _ = Token.objects.get_or_create(user=check_user)
                login(self.request, check_user)
                data = Response({'ur_t': get_token.key})
                data.set_cookie('ur_t', get_token.key)
                return data
            return Response({'status': False, 'msg': 'your password is worng'})
        return Response({'status': False, 'msg': 'please provide correct data'})

class ListUsersListAPIView(ListAPIView):
    # permission_classes = (UserListPermissionReadOnly,)
    queryset = User.objects.all()
    serializer_class = UsersModelSerializer

class UserRolesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        roles_data = dict(User.user_choice)
        return Response({'data': roles_data, 'error': [], 'status': True})

class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer_var = self.serializer_class(data, many=True)
        return Response({'data': serializer_var.data, "error": [], "status": True})
        self.get_serializer()

class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def list(self, request, *args, **kwargs):
        country_var = int(self.kwargs.get('country', None))
        if country_var is not None:
            data = self.queryset.filter(
                country__id = country_var
            )
            serializer_var = self.serializer_class(data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})

class StateListAPIView(ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def list(self, request, *args, **kwargs):
        country_var = int(self.kwargs.get('country', None))
        region_var = int(self.kwargs.get('region', None))
        if country_var and region_var is not None:
            data = self.queryset.filter(
                region__country__id = country_var,
                region__id = region_var
            )
            serializer_var = self.serializer_class(data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})

class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        country_var = int(self.kwargs.get('country', None))
        region_var = int(self.kwargs.get('region', None))
        state_var = int(self.kwargs.get('state', None))
        if country_var and region_var and state_var is not None:
            data = self.queryset.filter(
                state__region__country__id = country_var,
                state__region__id = region_var,
                state__id = state_var
            )
            serializer_var = self.serializer_class(data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})

class CenterListAPIView(ListAPIView):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer

    def list(self, request, *args, **kwargs):
        country_var = int(self.kwargs.get('country', None))
        region_var = int(self.kwargs.get('region', None))
        state_var = int(self.kwargs.get('state', None))
        city_var = int(self.kwargs.get('city', None))
        if country_var and region_var and state_var and city_var is not None:
            data = self.queryset.filter(
                city__state__region__country__id = country_var,
                city__state__region__id = region_var,
                city__state__id = state_var,
                city__id = city_var
            )
            serializer_var = self.serializer_class(data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})

class DesignationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get("action"):

            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= Designation.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = DesignationSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = Designation.objects.all().order_by("-id")
                        page = int(req_paginations['page'])
                        if page!=0:
                            paginator = Paginator(req_all_obj,2)
                            try:
                                users = paginator.page(page)
                            except PageNotAnInteger:
                                users = paginator.page(1)
                            except EmptyPage:
                                users = paginator.page(paginator.num_pages)
                            batch_numpages = paginator.num_pages
                            if batch_numpages > 0:
                                batch_numpage =  batch_numpages
                                batch_next = users.has_next()
                                batch_previous = users.has_previous()
                                batch_user_changes = users.has_other_pages()
                                if page >1:
                                    batch_previous_page = users.previous_page_number()
                                    current_page = users.number
                                else:
                                    batch_previous_page = 1
                                    current_page = 1
                                batch_index = users.start_index()
                                batch_end = users.end_index()
                                batchee = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                                "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                                "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}

                            else:
                                batchee = {"batch_numpage":batch_numpages}

                            serializer_obj = DesignationSerializer(users,many=True)
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = Designation.objects.all().order_by("-id")
                            serializer_var = DesignationSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    designation = self.request.data.get("designation")
                    designation = designation.strip()
                    if len(designation) != 0:
                        req_obj = Designation.objects.get_or_create(designation=designation)
                        serializer_var = DesignationSerializer(req_obj[0])
                        if req_obj[1]==False:
                            return Response(data={"data":{},"error":["record already exists"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        elif req_obj[1]==True:
                            return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide valid input"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except KeyError as e:
                    error_statement = str(e).strip("'")+" is missing"
                    error = []
                    error.append(error_statement)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError as e:
                    error = []
                    error_statment = str(e).split(" ")[1].strip("'")+" datatypes are not matching"
                    error.append(error_statment)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    req_attr_designation = req_data.get("designation")
                    req_attr_designation = req_attr_designation.strip()
                    if len(req_attr_designation) != 0:
                        try:
                            req_update_object = Designation.objects.get(designation= req_attr_designation)
                            return Response(data={"data":{},"error":["same record found"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            updatable = ["designation"]
                            if "id" in req_data:
                                req_id = req_data["id"]
                                try:
                                    req_obj = Designation.objects.get(id=req_id)
                                except:
                                    return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                                for attr in updatable :
                                    if attr in req_data :
                                        setattr(req_obj,attr,req_data[attr])
                                req_obj.save()
                                serializer_var = DesignationSerializer(req_obj)
                                return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                            else:
                                return Response(data={"data":{},"error":["id is not provided"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="remove":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    if "id" in req_data :
                        req_id = req_data["id"]
                        try:
                            req_obj = Designation.objects.get(id=req_id)
                            req_obj.delete()
                            return Response(data={"data":{},"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

        else:
            return Response(data={"data":{},"error":"please provide action","status":False, "paginations":{}},status=status.HTTP_200_OK)

class EmployementTypeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= EmploymentType.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = EmploymentTypeSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = EmploymentType.objects.all().order_by("-id")
                        page = int(req_paginations['page'])
                        if page!=0:
                            paginator = Paginator(req_all_obj,2)
                            try:
                                users = paginator.page(page)
                            except PageNotAnInteger:
                                users = paginator.page(1)
                            except EmptyPage:
                                users = paginator.page(paginator.num_pages)
                            batch_numpages = paginator.num_pages
                            if batch_numpages > 0:
                                batch_numpage =  batch_numpages
                                batch_next = users.has_next()
                                batch_previous = users.has_previous()
                                batch_user_changes = users.has_other_pages()
                                if page >1:
                                    batch_previous_page = users.previous_page_number()
                                    current_page = users.number
                                else:
                                    batch_previous_page = 1
                                    current_page = 1
                                batch_index = users.start_index()
                                batch_end = users.end_index()
                                batchee = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                                "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                                "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}

                            else:
                                batchee = {"batch_numpage":batch_numpages}

                            serializer_obj = EmploymentTypeSerializer(users,many=True)
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = EmploymentType.objects.all().order_by("-id")
                            serializer_var = EmploymentTypeSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    employement_type = self.request.data.get("et_name")
                    employement_type = employement_type.strip()
                    if len(employement_type) != 0:
                        req_obj = EmploymentType.objects.get_or_create(et_name=employement_type)
                        serializer_var = EmploymentTypeSerializer(req_obj[0])
                        if req_obj[1]==False:
                            return Response(data={"data":{},"error":["record already exists"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        elif req_obj[1]==True:
                            return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide valid input"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except KeyError as e:
                    error_statement = str(e).strip("'")+" is missing"
                    error = []
                    error.append(error_statement)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError as e:
                    error = []
                    error_statment = str(e).split(" ")[1].strip("'")+" datatypes are not matching"
                    error.append(error_statment)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    req_attr_et = req_data.get("et_name")
                    req_attr_et = req_attr_et.strip()
                    if len(req_attr_et) != 0:
                        try:
                            req_update_object = EmploymentType.objects.get(et_name= req_attr_et)
                            return Response(data={"data":{},"error":["same record found"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            updatable = ["et_name"]
                            if "id" in req_data:
                                req_id = req_data["id"]
                                try:
                                    req_obj = EmploymentType.objects.get(id=req_id)
                                except:
                                    return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                                for attr in updatable :
                                    if attr in req_data :
                                        setattr(req_obj,attr,req_data[attr])
                                req_obj.save()
                                serializer_var = EmploymentTypeSerializer(req_obj)
                                return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                            else:
                                return Response(data={"data":{},"error":["id is not provided"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="remove":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    if "id" in req_data :
                        req_id = req_data["id"]
                        print("id is",type(req_id))
                        try:
                            req_obj = EmploymentType.objects.get(id=req_id)
                            req_obj.delete()
                            return Response(data={"data":{},"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

        else:
            return Response(data={"data":{},"error":"please provide action","status":False, "paginations":{}},status=status.HTTP_200_OK)

class DivisionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= Division.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = DivisionSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = Division.objects.all().order_by('-id')
                        page = int(req_paginations['page'])
                        if page!=0:
                            paginator = Paginator(req_all_obj,2)
                            try:
                                users = paginator.page(page)
                            except PageNotAnInteger:
                                users = paginator.page(1)
                            except EmptyPage:
                                users = paginator.page(paginator.num_pages)
                            batch_numpages = paginator.num_pages
                            if batch_numpages > 0:
                                batch_numpage =  batch_numpages
                                batch_next = users.has_next()
                                batch_previous = users.has_previous()
                                batch_user_changes = users.has_other_pages()
                                if page >1:
                                    batch_previous_page = users.previous_page_number()
                                    current_page = users.number
                                else:
                                    batch_previous_page = 1
                                    current_page = 1
                                batch_index = users.start_index()
                                batch_end = users.end_index()
                                batchee = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                                "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                                "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}

                            else:
                                batchee = {"batch_numpage":batch_numpages}

                            serializer_obj = DivisionSerializer(users,many=True)
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = Division.objects.all().order_by('-id')
                            serializer_var = DivisionSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    division = self.request.data.get("division")
                    division = division.strip()
                    if len(division) != 0:
                        req_obj = Division.objects.get_or_create(division=division)
                        serializer_var = DivisionSerializer(req_obj[0])
                        if req_obj[1]==False:
                            return Response(data={"data":{},"error":["record already exists"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        elif req_obj[1]==True:
                            return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide valid input"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except KeyError as e:
                    error_statement = str(e).strip("'")+" is missing"
                    error = []
                    error.append(error_statement)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError as e:
                    error = []
                    error_statment = str(e).split(" ")[1].strip("'")+" datatypes are not matching"
                    error.append(error_statment)
                    return Response(data={"data":{},"error":error,"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    req_attr_division = req_data.get("division")
                    req_attr_division = req_attr_division.strip()
                    if len(req_attr_division) != 0:
                        try:
                            req_update_object = Division.objects.get(division= req_attr_division)
                            return Response(data={"data":{},"error":["record already exists"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            updatable = ["division"]
                            if "id" in req_data:
                                req_id = req_data["id"]
                                try:
                                    req_obj = Division.objects.get(id=req_id)
                                except:
                                    return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                                for attr in updatable :
                                    if attr in req_data :
                                        setattr(req_obj,attr,req_data[attr])
                                req_obj.save()
                                serializer_var = DivisionSerializer(req_obj)
                                return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                            else:
                                return Response(data={"data":{},"error":["id is not provided"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="remove":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    if "id" in req_data :
                        req_id = req_data["id"]
                        try:
                            req_obj = Division.objects.get(id=req_id)
                            req_obj.delete()
                            return Response(data={"data":{},"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

        else:
            return Response(data={"data":{},"error":"please provide action","status":False, "paginations":{}},status=status.HTTP_200_OK)

class DepartmentAPIView(APIView):
    serializer_class = DepartmentSerializer
    queryset_var = Departments.objects.all()
    def post(self, request, *args, **kwargs):
        self.post_parameter = self.request.data
        get_action_function = get_action(self.post_parameter.get('action', None))
        if get_action_function:
            func = getattr(self, get_action_function)
            return func(self.request)
        return Response({'data': [], 'error': 'please mention your action', 'status': False})

    def create(self, request, *args, **kwargs):
        fields_response = self.request.data.get('fields', None)
        create_data = self.request.data.get('data', None)
        if fields_response and create_data:
            fields_response = fields_response.split()
            create_data = loads(create_data)
            exclude_fields = ['users', 'created_on', 'created_by']
            department_instance = Departments()
            model_fields = [i.name for i in Departments._meta.get_fields() if i.name not in exclude_fields]
            for key, value in create_data.items():
                if key in model_fields:
                    setattr(department_instance, key, value)
            department_instance.save()
            return self.retrieve(self.request, department_instance)
        return Response({'data': [], 'error': 'please givin the corrent data', 'status': False})

    def delete(self, request, *args, **kwargs):
        fields_response = self.request.data.get('fields', None)
        condition_data = self.request.data.get('conditions', None)
        if fields_response and condition_data:
            fields_response = self.request.data['fields'].split()
            condition_data = loads(self.request.data['conditions'])
            department_instance = Departments.objects.get(id = condition_data.get('id')).delete()
            return self.retrieve(self.request)
        return Response({'data': [], 'error': 'please provide condition with id', 'status': False})

    def patch(self, request, *args, **kwargs):
        fields_response = self.request.data.get('fields', None)
        condition_data = self.request.data.get('conditions', None)
        update_data = self.request.data.get('data', None)
        if update_data and condition_data:
            fields_response = fields_response.split()
            condition_data = loads(condition_data)
            update_data = loads(update_data)
            data_instance = self.queryset_var.get(id = int(condition_data['id']))
            exclude_fields = ['users', 'created_on', 'created_by']
            model_fields = [i.name for i in Departments._meta.get_fields() if i.name not in exclude_fields]
            for key, value in update_data.items():
                if key in model_fields:
                    setattr(data_instance, key, value)
            data_instance.save()
            return self.retrieve(self.request, data_instance)
        return Response({'data': [], 'error': 'please givin the corrent data', 'status': False})

    def view(self, request, *args, **kwargs):
        if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= Departments.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = DepartmentSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = Departments.objects.all().order_by("-id")
                        page = int(req_paginations['page'])
                        if page!=0:
                            paginator = Paginator(req_all_obj,2)
                            try:
                                users = paginator.page(page)
                            except PageNotAnInteger:
                                users = paginator.page(1)
                            except EmptyPage:
                                users = paginator.page(paginator.num_pages)
                            batch_numpages = paginator.num_pages
                            if batch_numpages > 0:
                                batch_numpage =  batch_numpages
                                batch_next = users.has_next()
                                batch_previous = users.has_previous()
                                batch_user_changes = users.has_other_pages()
                                if page >1:
                                    batch_previous_page = users.previous_page_number()
                                    current_page = users.number
                                else:
                                    batch_previous_page = 1
                                    current_page = 1
                                batch_index = users.start_index()
                                batch_end = users.end_index()
                                batchee = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                                "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                                "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}

                            else:
                                batchee = {"batch_numpage":batch_numpages}

                            serializer_obj = DepartmentSerializer(users,many=True)
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = Departments.objects.all().order_by("-id")
                            serializer_var = DepartmentSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)
        # if self.request.data.get('fields', None):
        #     fields_data = self.request.data['fields'].split()
        #     department_data = Departments.objects.all().values(*fields_data)
        #     serializer_var = self.serializer_class(department_data, many=True)
        #     return Response({'data': serializer_var.data, 'error': [], 'status': True})
        # return Response({'data': [], 'error': 'please provide fields', 'status': False})

    def retrieve(self, request, data=None, *args, **kwargs):
        if self.request.data.get('fields', None) and data:
            fields_data = self.request.data['fields'].split()
            department_data = Departments.objects.filter(id = data.id).values(*fields_data)
            serializer_var = self.serializer_class(department_data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})
        elif self.request.data.get('fields', None):
            fields_data = self.request.data['fields'].split()
            department_data = Departments.objects.all().values(*fields_data)
            serializer_var = self.serializer_class(department_data, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})
        else:
            return Response({'data': [], 'error': 'please provide fields', 'status': False})

class ConceptsAPIView(APIView):
    serializer_class = ConceptSerializer
    def post(self, request, *args, **kwargs):
        pass

class SkillAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= Skill.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = SkillSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = Skill.objects.all().order_by("-id")
                        page = int(req_paginations['page'])
                        if page!=0:
                            paginator = Paginator(req_all_obj,2)
                            try:
                                users = paginator.page(page)
                            except PageNotAnInteger:
                                users = paginator.page(1)
                            except EmptyPage:
                                users = paginator.page(paginator.num_pages)
                            batch_numpages = paginator.num_pages
                            if batch_numpages > 0:
                                batch_numpage =  batch_numpages
                                batch_next = users.has_next()
                                batch_previous = users.has_previous()
                                batch_user_changes = users.has_other_pages()
                                if page >1:
                                    batch_previous_page = users.previous_page_number()
                                    current_page = users.number
                                else:
                                    batch_previous_page = 1
                                    current_page = 1
                                batch_index = users.start_index()
                                batch_end = users.end_index()
                                batchee = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                                "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                                "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}

                            else:
                                batchee = {"batch_numpage":batch_numpages}

                            serializer_obj = SkillSerializer(users,many=True)
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = Skill.objects.all().order_by("-id")
                            serializer_var = SkillSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    skill = self.request.data.get("skill")
                    subject = self.request.data.get("subject")
                    skill=skill.strip()
                    subject=subject.strip()
                    if len(skill) != 0 and len(subject)!=0:
                        req_obj = Skill.objects.get_or_create(skill=skill,subject=subject)
                        serializer_var = SkillSerializer(req_obj[0])
                        if req_obj[1]==False:
                            return Response(data={"data":{},"error":["record already exists"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        elif req_obj[1]==True:
                            return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide valid input"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except KeyError as e:
                    error_statement = str(e).strip("'")+" is missing"
                    error = []
                    error.append(error_statement)
                    return Response(data={"data":{},"error":error,"status":False},status=status.HTTP_200_OK)

                except ValueError as e:
                    error = []
                    error_statment = str(e).split(" ")[1].strip("'")+" datatypes are not matching"
                    error.append(error_statment)
                    return Response(data={"data":{},"error":error,"status":False},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["skill","subject"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = Skill.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = SkillSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["id is not provided"],"status":False},status=status.HTTP_200_OK)
                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False},status=status.HTTP_200_OK)

            elif request.data.get("action")=="remove":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    if "id" in req_data :
                        req_id = req_data["id"]
                        try:
                            req_obj = Skill.objects.get(id=req_id)
                            req_obj.delete()
                            return Response(data={"data":{},"error":[],"status":True},status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False},status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False},status=status.HTTP_200_OK)

                except TypeError:
                    return Response(data={"data":{},"error":["please check whether you are providing conditions"],"status":False},status=status.HTTP_200_OK)

        else:
            return Response(data={"data":{},"error":"please provide action","status":False},status=status.HTTP_200_OK)

class FacultyAPIVIew(APIView):
    def post(self, request, *args, **kwargs):
        self.post_parameter = self.request.data
        get_action_function = get_action(self.post_parameter.get('action', None))
        if get_action_function:
            func = getattr(self, get_action_function)
            return func(self.request)
        return Response({'data': [], 'error': 'please mention your action', 'status': False})

    def create(self, request, *args, **kwargs):
        create_data = self.request.data.get('data', None)
        if create_data:
            create_data = loads(self.request.data['data'])
            name_var = create_data.get('name', None)
            subjects = list(create_data.get('subject', None))
            role_var = int(create_data.get('role', None))
            department_var = create_data.get('department', None)
            designation = create_data.get('designation', None)
            et = create_data.get('etname', None)
            skill = create_data.get('skill', None)
            batches = create_data.get('batches', None)
            country = create_data.get('country', None)
            region = create_data.get('region', None)
            state = create_data.get('state', None)
            city = create_data.get('city', None)
            center_var = create_data.get('center', None)
            password_var = "python@123"
            email_var = '{}@goognu.com'.format(name_var)
            try:
                user_create = User.objects.create_user(
                    name_var,
                    email=email_var,
                    password=password_var,
                    roles=role_var)
            except:
                user_create = User.objects.get(username=name_var)
            faculty_user_create = Faculties.objects.get_or_create(
                    user_id=user_create.id,
                    name = name_var,
                    center_id = int(center_var))
            faculty_subjects = [Facultyhassubjects(faculty_id=faculty_user_create[0].id, subject=int(i)) for i in subjects]
            faculty_subject_create = Facultyhassubjects.objects.bulk_create(faculty_subjects)
            department_objs = [DepartmentMapping(department_id=int(i), user_id=faculty_user_create[0].id) for i in department_var]
            department_create = DepartmentMapping.objects.bulk_create(department_objs)
            designation_objs = [DesignationMapping(designation_id=int(i), user_id=faculty_user_create[0].id) for i in designation]
            designation_create = DesignationMapping.objects.bulk_create(designation_objs)
            employment_obj = [EmploymentTypeMapping(employment_id=int(i), user_id=faculty_user_create[0].id) for i in et]
            employment_create = EmploymentTypeMapping.objects.bulk_create(employment_obj)
            batch_objs = [UserBatch(batch=int(i), user_id=faculty_user_create[0].id) for i in batches]
            batch_create_user = UserBatch.objects.bulk_create(batch_objs)
            return Response({'data': [], 'error': [], 'status': True})

    def patch(self, request, *args, **kwargs):
        conditions_data = self.request.data.get('conditions', None)
        update_data = self.request.data.get('data', None)
        if conditions_data and update_data:
            conditions_data = loads(self.request.data['conditions'])
            update_data = loads(self.request.data['data'])
            name_var = create_data.get('name', None)
            subjects = list(create_data.get('subject', None))
            role_var = int(create_data.get('role', None))
            department_var = create_data.get('department', None)
            designation = create_data.get('designation', None)
            et = create_data.get('etname', None)
            skill = create_data.get('skill', None)
            batches = create_data.get('batches', None)
            country = create_data.get('country', None)
            region = create_data.get('region', None)
            state = create_data.get('state', None)
            city = create_data.get('city', None)
            center_var = create_data.get('center', None)
            faculty_data = Faculties.objects.filter(id=conditions_data['id'])
            user_model = User.objects.get(id=faculty_data[0].id)
            # user_model.username
            faculty_data.update(
                name=name_var,
                center_id=int(center_var))
        return Response({'data': [], 'error': "Please provide data and conditions", 'status': False})

    def delete(self, request, *args, **kwargs):
        if self.request.data.get('conditions', None):
            conditions_data = loads(self.request.data['conditions'])
            student_data = Faculties.objects.get(id = conditions_data['id'])
            student_data.status = True
            student_data.save()
            return Response({'data': [], 'error': [], 'status': True})
        return Response({'data': [], 'error': "Please provide conditions", 'status': False})

    def view(self, request, *args, **kwargs):
        queryset = Faculties.objects.all()
        if self.request.data.get('conditions', None):
            get_id = loads(self.request.data['conditions'])
            filter_data = queryset.filter(id = get_id['id'])
            serializer_var = FacultiesSerializer(filter_data, many=True)
            faculties_id = serializer_var.data[0]['id']
            department_filter = DepartmentMapping.objects.filter(user_id=faculties_id)
            designation_filter = DesignationMapping.objects.filter(user_id=faculties_id)
            employment_filter = EmploymentTypeMapping.objects.filter(user_id=faculties_id)
            user_subjects = Facultyhassubjects.objects.filter(faculty_id=faculties_id)
            for p in serializer_var.data:
                p['department'] = []
                p['designation'] = []
                p['employment_type'] = []
                p['subjects'] = []
                for i in department_filter:
                    p['department'].append({'id': i.department.id, 'department': i.department.department})
                for i in designation_filter:
                    p['designation'].append({'id': i.designation.id, 'designation': i.designation.designation})
                for i in employment_filter:
                    p['employment_type'].append({'id': i.employment.id, 'type': i.employment.et_name})
                for i in user_subjects:
                    p['subjects'].append({'id': i.id, 'subject': i.subject})
                return Response({'data': serializer_var.data, 'error': [], 'status': True})
        else:
            check_pagination = pagination_function(request=self.request, data=queryset.filter(status = False).order_by('-id'))
            if check_pagination['data'] != 404:
                serializer_var = FacultiesSerializer(check_pagination['data'], many=True)
                for i in serializer_var.data:
                    i['num_pages'] = check_pagination.get('num_pages', None)
                for p in serializer_var.data:
                    department_filter = DepartmentMapping.objects.filter(user_id=p['id'])
                    designation_filter = DesignationMapping.objects.filter(user_id=p['id'])
                    employment_filter = EmploymentTypeMapping.objects.filter(user_id=p['id'])
                    subjects_filter = Facultyhassubjects.objects.filter(faculty_id=p['id'])
                    user_batch_filter = UserBatch.objects.filter(user_id=p['id'])
                    p['department'] = []
                    for i in department_filter:
                        p['department'].append({'id': i.department.id, 'department': i.department.department})
                    p['designation'] = []
                    for i in designation_filter:
                        p['designation'].append({'id': i.designation.id, 'designation': i.designation.designation})
                    p['employment_type'] = []
                    for i in employment_filter:
                        p['employment_type'].append({'id': i.employment.id, 'type': i.employment.et_name})
                    p['subjects'] = []
                    for i in subjects_filter:
                        p['subjects'].append({'id': i.id, 'subject': i.subject})
                    p['batches'] = []
                    for i in user_batch_filter:
                        p['batches'].append({'id': i.id, 'batch': i.batch})
                return Response({'data': serializer_var.data, 'error': [], 'status': True})
            return Response({'data': [], 'error': 'Please provide pagination number', 'status': False})

class CenterAPIView(APIView):
    queryset_var = Center.objects.all()
    serializer_class = CenterSerializer
    def post(self, request, *args, **kwargs):
        self.post_parameter = self.request.data
        get_action_function = get_action(self.post_parameter.get('action', None))
        if get_action_function:
            func = getattr(self, get_action_function)
            return func(self.request)
        return Response({'data': [], 'error': 'please mention your action', 'status': False})

    def create(self, request, *args, **kwargs):
        if self.request.data.get('data', None):
            create_data = loads(self.request.data['data'])
            city = int(create_data['city'])
            center_name_var = create_data['center']
            center_create_data = Center.objects.create(
                    city_id=city,
                    center_name=center_name_var)
            return Response({'data': [], 'error': [], 'status': True})
        return Response({'data': [], 'error': [], 'status': False})

    def patch(self, request, *args, **kwargs):
        conditions_data = self.request.data.get('conditions', None)
        update_data = self.request.data.get('data', None)
        if conditions_data and update_data:
            conditions_data = loads(self.request.data['conditions'])
            update_data = loads(self.request.data['data'])
            center_id = int(conditions_data['id'])
            country_id = int(update_data['country_edit'])
            region_id = int(update_data['region_edit'])
            state_id = int(update_data['state_edit'])
            city_id = int(update_data['city_edit'])
            center_name_var = update_data['center_edit']
            center_obj = Center.objects.get(id=center_id)
            center_obj.center_name=center_name_var
            center_obj.city_id=city_id
            center_obj.save()
            get_city = City.objects.get(id=city_id)
            get_city.state_id=state_id
            get_city.save()
            get_state = State.objects.get(id=state_id)
            get_state.region_id = region_id
            get_state.save()
            get_region = Region.objects.get(id=region_id)
            get_region.country_id = country_id
            get_region.save()
            return Response({'data': [], 'error': [], 'status': True})
        return Response({'data': [], 'error': [], 'status': False})

    def view(self, request, *args, **kwargs):
        if self.request.data.get('conditions', None):
            condition_data = loads(self.request.data['conditions'])
            center_filter = self.queryset_var.filter(id = int(condition_data['id']))
            serializer_var = CenterSerializer(center_filter, many=True)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})
        center_filter = self.queryset_var.filter(status = False).order_by('-id')
        check_pagination = pagination_function(request=self.request, data=center_filter)
        if check_pagination['data'] != 404:
            serializer_var = CenterSerializer(check_pagination['data'], many=True)
            for i in serializer_var.data:
                i['num_pages'] = check_pagination.get('num_pages', None)
            return Response({'data': serializer_var.data, 'error': [], 'status': True})
        return Response({'data': [], 'error': 'Please provide pagination number', 'status': False})

    def delete(self, request, *args, **kwargs):
        if self.request.data.get('conditions[id]', None):
            condition_data = loads(self.request.data['conditions[id]'])
            center_data = Center.objects.get(id = condition_data)
            center_data.status = True
            center_data.save()
            return Response({'data': [], 'error': [], 'status': True})
        return Response({'data': [], 'error': "Please give conditions with id", 'status': False})

class StudentAPIView(APIView):
    queryset_var = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer
    def post(self, request, *args, **kwargs):
        self.post_parameter = self.request.data
        get_action_function = get_action(self.post_parameter.get('action', None))
        if get_action_function:
            func = getattr(self, get_action_function)
            return func(self.request)
        return Response({'data': [], 'error': 'please mention your action', 'status': False})

    def create(self, request, *args, **kwargs):
        if self.request.data.get('data', None):
            create_data = loads(self.request.data['data'])
            student_user_name = create_data['name']
            student_email = create_data['student_email']
            student_mobile = create_data['student_mobile']
            student_dob = create_data['student_dob']
            #
            # datetime_dob_date = datetime.strptime(student_dob, "%m/%d/%Y").date()
            # student_dob_data = datetime_dob_date.strftime('%Y-%m-%d')
            #
            gender = create_data['gender']
            phase_start_date = create_data['phase_start_date']
            #
            # phase_date_for = datetime.strptime(student_dob, "%m/%d/%Y").date()
            # phase_finial = datetime_dob_date.strftime('%Y-%m-%d')
            #
            division = create_data['division']
            phase = create_data['phase']
            session = create_data['session']
            program = create_data['program']
            initial_batch = create_data['initial_batch']
            current_batch = create_data['current_batch']
            pervious_batch = create_data['pervious_batch']
            student_class = create_data['class']
            student_center = create_data['center']
            subject = create_data['subject']
            medium = create_data['medium']
            role_number = create_data['role_number']
            father_name = create_data['father_name']
            father_email = create_data['father_email']
            father_mobile = create_data['father_mobile']
            mother_name = create_data['mother_name']
            mother_email = create_data['mother_email']
            mother_mobile = create_data['mother_mobile']
            try:
                student_user_creation = User.objects.create_user(
                        student_user_name,
                        email=student_email,
                        password="python@123",
                        roles=4)
            except:
                student_user_creation = User.objects.get(username=student_user_name)
            studentinfo_creation = StudentInfo.objects.create(
                        user_id=student_user_creation.id,
                        name=student_user_name,
                        email=student_email,
                        phone=student_mobile,
                        gender=gender,
                        division=division,
                        dob=student_dob,
                        role_number=role_number,
                        phase=phase,
                        phase_start_date=phase_start_date,
                        medium=medium,
                        center = student_center,
                        inital_batch=initial_batch,
                        current_batch=current_batch,
                        previous_batch=pervious_batch,
                        student_class=student_class,
                        student_program=program,
                        session=session,
                        father_name=father_name,
                        father_email=father_email,
                        father_mobile=father_mobile,
                        mother_name=mother_name,
                        mother_email=mother_email,
                        mother_mobile=mother_mobile)
            StudentHasSubjectsObjs = [StudentHasSubjects(student_id=studentinfo_creation.id, subject=i) for i in subject]
            SubjectBulkCreate = StudentHasSubjects.objects.bulk_create(StudentHasSubjectsObjs)
            serializer_var = self.serializer_class(studentinfo_creation, many=True)
            return Response({'data': [], 'error': [], 'status': True})

    def patch(self, request, *args, **kwargs):
        if self.request.data.get('data', None) and self.request.data.get('conditions', None):
            conditions_data = loads(self.request.data['conditions'])
            update_data = loads(self.request.data['data'])
            student_user_name = update_data['name']
            student_email = update_data['student_email']
            student_mobile = update_data['student_mobile']
            student_dob = update_data['student_dob']
            #
            # datetime_dob_date = datetime.strptime(student_dob, "%m/%d/%Y").date()
            # student_dob_data = datetime_dob_date.strftime('%Y-%m-%d')
            #
            gender = update_data['gender']
            phase_start_date = update_data['phase_start_date']
            #
            # phase_date_for = datetime.strptime(student_dob, "%m/%d/%Y").date()
            # phase_finial = datetime_dob_date.strftime('%Y-%m-%d')
            #
            division = update_data['division']
            phase = update_data['phase']
            session = update_data['session']
            program = update_data['program']
            initial_batch = update_data['initial_batch']
            current_batch = update_data['current_batch']
            pervious_batch = update_data['pervious_batch']
            student_class = update_data['class']
            # subject = update_data['subject']
            medium = update_data['medium']
            role_number = update_data['role_number']
            father_name = update_data['father_name']
            father_email = update_data['father_email']
            father_mobile = update_data['father_mobile']
            mother_name = update_data['mother_name']
            mother_email = update_data['mother_email']
            mother_mobile = update_data['mother_mobile']
            student_data = StudentInfo.objects.filter(id = int(conditions_data['id']))
            student_data.update(
                name=student_user_name,
                email=student_email,
                phone=student_mobile,
                gender=gender,
                division=division,
                dob=student_dob,
                role_number=role_number,
                phase=phase,
                phase_start_date=phase_start_date,
                medium=medium,
                inital_batch=initial_batch,
                current_batch=current_batch,
                previous_batch=pervious_batch,
                student_class=student_class,
                student_program=program,
                session=session,
                father_name=father_name,
                father_email=father_email,
                father_mobile=father_mobile,
                mother_name=mother_name,
                mother_email=mother_email,
                mother_mobile=mother_mobile)
            return Response({'data': [], 'error': [], 'status': True})

    def view(self, request, *args, **kwargs):
        if self.request.data.get('conditions', None):
            conditions_data = loads(self.request.data['conditions'])
            student_user_filter = self.queryset_var.get(
                    id=conditions_data['id'])
            get_center = Center.objects.get(id = student_user_filter.center)
            center_serializer_data = CenterSerializer(get_center)
            serializer_var = self.serializer_class(student_user_filter)
            serializer_var.data['center_data'] = center_serializer_data.data
            return Response({'data': serializer_var.data, 'error': [], 'status': True})
        else:
            if self.request.data.get('pagination', None):
                student_user_filter = self.queryset_var.filter(status=False).order_by('-id')
                check_pagination = pagination_function(request=self.request, data=student_user_filter)
                if check_pagination['data'] != 404:
                    serializer_var = StudentInfoSerializerOnly(check_pagination['data'], many=True)
                    for i in serializer_var.data:
                        i['num_pages'] = check_pagination.get('num_pages', None)
                    return Response({'data': serializer_var.data, 'error': [], 'status': True})
                return Response({'data': [], 'error': 'Please provide pagination number', 'status': False})
            return Response({'data': [], 'error': 'Please provide pagination number', 'status': False})

    def delete(self, request, *args, **kwargs):
        if self.request.data.get('conditions', None):
            conditions_data = loads(self.request.data.get('conditions'))
            get_student_data = StudentInfo.objects.get(id = conditions_data['id'])
            get_student_data.status = True
            get_student_data.save()
            return Response({'data': [], 'error': [], 'status': True})
        return Response({'data': [], 'error': [], 'status': False})
