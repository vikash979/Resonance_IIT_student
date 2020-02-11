from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.subject_micro import subject_to_class

def page_filter(filter_obj):
    id=[]
    for i in filter_obj:
        id.append(i.class_id)

    req_class_obj = subject_to_class(id)
    for name in req_class_obj:
        for obj in filter_obj:
            if name["id"] == obj.class_id:
                obj.class_name = name["name"]
    return filter_obj

class MasterSubjectApiView(APIView):

    def post(self, request, *args, **kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= MasterSubjects.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = MasterSubjectSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        req_all_obj = MasterSubjects.objects.all().order_by('-id')
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

                            serializer_obj = MasterSubjectSerializer(users,many=True)  
                            return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                        elif page==0:
                            req_all_obj = MasterSubjects.objects.all().order_by('-id')
                            serializer_var = MasterSubjectSerializer(req_all_obj,many=True)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)


            elif request.data.get("action")=="add":
                try:
                    name = self.request.data.get("name")
                    short_code = self.request.data.get("short_code")
                    description = self.request.data.get("description")
                    name = name.strip()
                    short_code = short_code.strip()
                    description = description.strip()
                    if len(name) != 0 and len(short_code)!=0 and len(description)!=0:
                        req_obj = MasterSubjects.objects.get_or_create(name=name,short_code=short_code,description=description)
                        serializer_var = MasterSubjectSerializer(req_obj[0])
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
                    req_attr_name = req_data.get("name")
                    req_attr_code = req_data.get("short_code")
                    req_attr_description = req_data.get("description")
                    req_attr_name=req_attr_name.strip()
                    req_attr_code = req_attr_code.strip()
                    req_attr_description = req_attr_description.strip()
                    if len(req_attr_name) != 0 and len(req_attr_code) != 0 and len(req_attr_description) != 0:
                        try:
                            req_update_object = MasterSubjects.objects.get(name=req_attr_name,short_code=req_attr_code,description=req_attr_description)
                            return Response(data={"data":{},"error":["same record found"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            updatable = ["name","description","short_code"]
                            if "id" in req_data:
                                req_id = req_data["id"]
                                try:
                                    req_obj = MasterSubjects.objects.get(id=req_id)
                                except:
                                    return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                                for attr in updatable :
                                    if attr in req_data :
                                        setattr(req_obj,attr,req_data[attr])
                                req_obj.save()
                                serializer_var = MasterSubjectSerializer(req_obj)
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
                            req_obj = MasterSubjects.objects.get(id=req_id)
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
   

class HasSubjectApiView(APIView):
    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")!=None and request.data.get("conditions")!=None :
                    req_conditions = json.loads(request.data.get("conditions"))
                    req_paginations = json.loads(request.data.get("paginations"))
                    if "id" in req_conditions and "page" not in req_paginations:
                        try:
                            req_obj= HasSubjects.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                            serializer_var = HasSubjectSerializer(req_obj)
                            return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                        except:
                            return Response(data={"data":[],"error":["no record found on provided id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

                    elif "id" not in req_conditions and "page" in req_paginations:
                        if "filter_by" not in req_conditions:
                            req_all_obj = HasSubjects.objects.all().order_by('-id')
                            page = int(req_paginations['page'])
                            if page!=0:
                                paginator = Paginator(req_all_obj,2)
                                try:
                                    id=[]
                                    users = paginator.page(page)
                                    for i in users:
                                        id.append(i.class_id)
                                
                                    req_class_obj = subject_to_class(id)
                                    for name in req_class_obj:
                                        for obj in users:
                                            if name["id"] == obj.class_id:
                                                obj.class_name = name["name"]
                                    
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

                                serializer_obj = HasSubjectSerializer(users,many=True)  
                                return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":batchee}, status=status.HTTP_200_OK)

                            elif page==0:
                                req_all_obj = HasSubjects.objects.all().order_by('-id')
                                serializer_var = HasSubjectSerializer(req_all_obj,many=True)
                                return Response(data={"data":serializer_var.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)

                        elif "filter_by" in req_conditions:
                            filter_by = req_conditions.get("filter_by")
                            if "class_id" in filter_by and "name" not in filter_by:
                                if int(filter_by.get("class_id"))!=0:
                                    filter_obj = HasSubjects.objects.filter(class_id=filter_by.get("class_id"))
                                    filter_obj=page_filter(filter_obj)
                                    serializer_obj = HasSubjectSerializer(filter_obj, many=True)
                                    return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                                elif int(filter_by.get("class_id"))==0:
                                    filter_obj= HasSubjects.objects.all()
                                    filter_obj=page_filter(filter_obj)
                                    serializer_obj= HasSubjectSerializer(filter_obj,many=True)
                                    return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                            elif "name" in filter_by and "class_id" not in filter_by:
                                filter_obj= HasSubjects.objects.filter(name__contains=filter_by.get("name"))
                                filter_obj=page_filter(filter_obj)
                                serializer_obj= HasSubjectSerializer(filter_obj,many=True)
                                return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                            elif "name" in filter_by and "class_id" in filter_by:
                                if int(filter_by.get("class_id"))!=0:
                                    filter_obj= HasSubjects.objects.filter(name__contains=filter_by.get("name"),class_id=filter_by.get("class_id"))
                                    filter_obj=page_filter(filter_obj)
                                    serializer_obj= HasSubjectSerializer(filter_obj,many=True)
                                    return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                                elif int(filter_by.get("class_id"))==0:
                                    filter_obj= HasSubjects.objects.all().filter(name__contains=filter_by.get("name"))
                                    filter_obj=page_filter(filter_obj)
                                    serializer_obj= HasSubjectSerializer(filter_obj,many=True)
                                    return Response(data={"data":serializer_obj.data,"error":[],"status":True,"paginations":{}}, status=status.HTTP_200_OK)
                    else:
                        return Response(data={"data":{},"error":["please provide id"],"status":False,"paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    name = self.request.data.get("name")
                    class_id = self.request.data["class_id"]
                    code = self.request.data["code"]
                    description = self.request.data.get("description")
                    master_subject = self.request.data["master_subject"]
                    name=name.strip()
                    class_id=class_id.strip()
                    code=code.strip()
                    description=description.strip()
                    master_subject=master_subject.strip()
                    if len(name) != 0 and len(code)!=0 and len(description)!=0 and len(class_id)!=0 and len(master_subject)!=0:
                        try:
                            req_master = MasterSubjects.objects.get(id=master_subject)
                        except:
                            return Response(data={"data":{},"error":["no record found on master_subject"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        req_obj = HasSubjects.objects.get_or_create(name=name,description=description,class_id=class_id,code=code,master_subject_id = master_subject )
                        serializer_var = HasSubjectSerializer(req_obj[0])
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
                    req_attr_name = req_data.get("name")
                    req_attr_code = req_data.get("code")
                    req_attr_description = req_data.get("description")
                    req_attr_class_id = req_data.get("class_id")
                    req_attr_master_id = req_data.get("master_subject_id")
                    req_attr_name=req_attr_name.strip()
                    req_attr_code=req_attr_code.strip()
                    req_attr_description=req_attr_description.strip()
                    req_attr_class_id=req_attr_class_id.strip()
                    req_attr_master_id=req_attr_master_id.strip()
                    if len(req_attr_name) != 0 and len(req_attr_code) != 0 and len(req_attr_description) != 0 and len(req_attr_class_id) != 0 and len(req_attr_master_id) != 0:
                        try:
                            req_update_object = HasSubjects.objects.get(name=req_attr_name,code=req_attr_code,description=req_attr_description, class_id=req_attr_class_id, master_subject_id=req_attr_master_id)
                            return Response(data={"data":{},"error":["same record found"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        except:
                            updatable = ["name","description","class_id","code","master_subject_id"]
                            if "id" in req_data:
                                req_id = req_data["id"]
                                master_subject_id = req_data["master_subject_id"]
                                try:
                                    req_obj = HasSubjects.objects.get(id=req_id)
                                    req_objmaster = MasterSubjects.objects.get(id=master_subject_id)
                                except:
                                    return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                                for attr in updatable :
                                    if attr in req_data :
                                        setattr(req_obj,attr,req_data[attr])
                                req_obj.save()
                                serializer_var = HasSubjectSerializer(req_obj)
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
                            req_obj = HasSubjects.objects.get(id=req_id)
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

class SubjectHasUnitApiView(APIView):
    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")==None:
                    all_obj = SubjectHasUnit.objects.all()
                    serializer_var = SubjectHasUnitSerializer(all_obj,many=True)
                    return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                else:
                    try:
                        req_obj= SubjectHasUnit.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                        serializer_var = SubjectHasUnitSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        return Response(data={"data":[],"error":["no record found on provided id"],"status":False, "paginations":{}}, status=status.HTTP_200_OK)
            
            elif request.data.get("action")=="add":
                try:
                    created_by = self.request.data["created_by"]
                    order = self.request.data["order"]
                    book_id = self.request.data["book_id"]
                    try:
                        req_obj = SubjectHasUnit.objects.get(order=order,book_id=book_id)
                        serializer_var = SubjectHasUnitSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    except:
                        req_obj = SubjectHasUnit.objects.create(order=order,book_id=book_id,created_by=created_by)
                        serializer_var = SubjectHasUnitSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                except KeyError:
                    return Response(data={"data":{},"error":["please check your credentials"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
            
            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["order","book_id"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = SubjectHasUnit.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = SubjectHasUnitSerializer(req_obj)
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
                            req_obj = SubjectHasUnit.objects.get(id=req_id)
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
    
class UnitHasChapterApiView(APIView):

    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")==None:
                    all_obj = UnitHasChapter.objects.all()
                    serializer_var = UnitHasChapterSerializer(all_obj,many=True)
                    return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                else:
                    try:
                        req_obj= UnitHasChapter.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                        serializer_var = UnitHasChapterSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        return Response(data={"data":[],"error":["no record found on provided id"],"status":False, "paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    created_by = self.request.data["created_by"]
                    order = self.request.data["order"]
                    subject_has_unit = self.request.data["subject_has_unit"]
                    try:
                        req_master = SubjectHasUnit.objects.get(id=subject_has_unit)
                    except:
                        return Response(data={"data":{},"error":["no record found on subject_has_unit"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                    try:
                        req_obj = UnitHasChapter.objects.get(order=order,subject_has_unit_id = subject_has_unit)
                        serializer_var = UnitHasChapterSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)
                    except:
                        req_obj = UnitHasChapter.objects.create(created_by=created_by,order=order,subject_has_unit_id = subject_has_unit)
                        serializer_var = UnitHasChapterSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}},status=status.HTTP_200_OK)

                except KeyError:
                    return Response(data={"data":{},"error":["please check your credentials"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["order"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = UnitHasChapter.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = UnitHasChapterSerializer(req_obj)
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
                            req_obj = UnitHasChapter.objects.get(id=req_id)
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
    
class ChapterHasTopicApiView(APIView):
    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")==None:
                    all_obj = ChapterHasTopic.objects.all()
                    serializer_var = ChapterHasTopicSerializer(all_obj,many=True)
                    return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                else:
                    try:
                        req_obj= ChapterHasTopic.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                        serializer_var = ChapterHasTopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        return Response(data={"data":[],"error":["no record found on provided id"],"status":False, "paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    created_by = self.request.data["created_by"]
                    order = self.request.data["order"]
                    unit_has_chapter = self.request.data["unit_has_chapter"]
                    try:
                        req_master = UnitHasChapter.objects.get(id=unit_has_chapter)
                    except:
                        return Response(data={"data":{},"error":["no record found on unit_has_chapter"],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    try:
                        req_obj = ChapterHasTopic.objects.get(order=order,unit_has_chapter_id = unit_has_chapter)
                        serializer_var = ChapterHasTopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        req_obj = ChapterHasTopic.objects.create(created_by=created_by,order=order,unit_has_chapter_id = unit_has_chapter)
                        serializer_var = ChapterHasTopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)

                except KeyError:
                    return Response(data={"data":{},"error":["please check your credentials"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["order"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = ChapterHasTopic.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = ChapterHasTopicSerializer(req_obj)
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
                            req_obj = ChapterHasTopic.objects.get(id=req_id)
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
        
class TopicHasSubtopicApiView(APIView):
    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")==None:
                    all_obj = TopicHasSubtopic.objects.all()
                    serializer_var = TopicHasSubtopicSerializer(all_obj,many=True)
                    return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                else:
                    try:
                        req_obj= TopicHasSubtopic.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                        serializer_var = TopicHasSubtopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        return Response(data={"data":[],"error":["no record found on provided id"],"status":False, "paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    created_by = self.request.data["created_by"]
                    order = self.request.data["order"]
                    chapter_has_topic = self.request.data["chapter_has_topic"]
                    level = self.request.data["level"]
                    try:
                        req_master = ChapterHasTopic.objects.get(id=chapter_has_topic)
                    except:
                        return Response(data={"data":{},"error":["no record found on chapter_has_topic"],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    try:
                        req_obj = TopicHasSubtopic.objects.get(order=order,chapter_has_topic_id=chapter_has_topic,level=level)
                        serializer_var = TopicHasSubtopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        req_obj = TopicHasSubtopic.objects.create(order=order,chapter_has_topic_id=chapter_has_topic,level=level,created_by=created_by)
                        serializer_var = TopicHasSubtopicSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)

                except KeyError:
                    return Response(data={"data":{},"error":["please check your credentials"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["order","chapter_has_topic_id","level"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = TopicHasSubtopic.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = TopicHasSubtopicSerializer(req_obj)
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
                            req_obj = TopicHasSubtopic.objects.get(id=req_id)
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

class TopicHasContentApiView(APIView):
    def post(self,request,*args,**kwargs):
        if request.data.get("action"):
            if request.data.get("action")=="view":
                if request.data.get("conditions")==None:
                    all_obj = TopicHasContent.objects.all()
                    serializer_var = TopicHasContentSerializer(all_obj,many=True)
                    return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                else:
                    try:
                        req_obj= TopicHasContent.objects.get(id=json.loads(request.data.get("conditions"))["id"])
                        serializer_var = TopicHasContentSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        return Response(data={"data":[],"error":["no record found on provided id"],"status":False, "paginations":{}}, status=status.HTTP_200_OK)

            elif request.data.get("action")=="add":
                try:
                    created_by = self.request.data["created_by"]
                    content = self.request.data["content"]
                    type = self.request.data["type"]
                    type_id = self.request.data["type_id"]
                    try:
                        req_obj = TopicHasContent.objects.get(content=content,type=type,type_id=type_id)
                        serializer_var = TopicHasContentSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                    except:
                        req_obj = TopicHasContent.objects.create(content=content,type=type,type_id=type_id,created_by=created_by)
                        serializer_var = TopicHasContentSerializer(req_obj)
                        return Response(data={"data":serializer_var.data,"error":[],"status":True, "paginations":{}}, status=status.HTTP_200_OK)
                
                except KeyError:
                    return Response(data={"data":{},"error":["please check your credentials"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

                except ValueError:
                    return Response(data={"data":{},"error":["input datatypes are not matching"],"status":False, "paginations":{}},status=status.HTTP_200_OK)

            elif request.data.get("action")=="update":
                try:
                    req_data = json.loads(request.data.get("conditions"))
                    updatable = ["content","type","type_id"]
                    if "id" in req_data:
                        req_id = req_data["id"]
                        try:
                            req_obj = TopicHasContent.objects.get(id=req_id)
                        except:
                            return Response(data={"data":{},"error":["no record found on id"],"status":False, "paginations":{}},status=status.HTTP_200_OK)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        serializer_var = TopicHasContentSerializer(req_obj)
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
                            req_obj = TopicHasContent.objects.get(id=req_id)
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