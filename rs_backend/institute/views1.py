from rest_framework import viewsets,filters
from rest_framework.response import Response
from django.contrib.auth.models import User
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import filters
from .models import Classs,Batches,StudentClassPath,Programhasclasses,Programs,PhaseHasSession,FacultyHasBatch,Sessions,Programclasshassubjects
from . import serializers



class ClasssViewset(viewsets.ModelViewSet):   
    queryset = Classs.objects.all()
    serializer_class = serializers.ClasssSerializer

    filter_backends = [filters.SearchFilter]
    filter_backends = [DjangoFilterBackend]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['display_name','programclassid__program__display_name']
    search_fields = ['name','programclassid__program__display_name','display_name']

    def pagination_data(self,class_numpages,users,page):
        
        if class_numpages > 0:
                class_numpage =  class_numpages
                
                
                #batch_range = "paginator.page_range"
                class_next = users.has_next()
                
                
                class_previous = users.has_previous()
                class_user_changes = users.has_other_pages()
                

                if class_next == True:
                    class_next_page_number = users.next_page_number()
                    
                
                if page >1:
                    class_previous_page = users.previous_page_number()
                    current_page = users.number
                else:
                    class_previous_page = 1
                    current_page = 1
                #print(current_page)
                class_index = users.start_index()
                class_end = users.end_index()
                if class_next != True:
                    
                    class_record = {"class_numpage":class_numpages,"class_next":class_next,
                    "class_previous":class_previous,"class_user_changes":class_user_changes,
                    "class_previous_page":class_previous_page,"class_index":class_index,"class_end":class_end,"current_page":current_page}
                else:
                    class_next_page_number = users.next_page_number()
                    class_record = {"class_numpage":class_numpages,"class_next":class_next,
                    "class_previous":class_previous,"class_user_changes":class_user_changes,
                    "class_previous_page":class_previous_page,"class_index":class_index,"class_end":class_end,"current_page":current_page,"class_next_page_number":class_next_page_number}
                
        else:
            class_record = {"class_numpage":class_numpages}
        return class_record
  
    def create(self, request): 
        data_error = []
       
            
        if request.data.get('action') =='add': 
            
            if len(data_error)==0:   
                
                 
                class_obj = Classs.objects.create(name=request.data['name'],display_name=request.data['display_name'],
                order=(request.data['order']),description=request.data['description'],
                ) 
                   
                serializer_obj=  serializers.ClasssSerializer(Classs.objects.all(),many=True)
                #print(serializer_obj.data)

                data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            else:

                 data= {"data":request.data,"status": False,"errors":data_error}
        elif request.data.get('action') =='view':
            if request.data.get('id')!= None:
                class_obj = Classs.objects.filter(id=request.data.get('id')) 
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    #class_obj = Classs.objects.filter(id=value)
                    if key=='id':
                        if isinstance(value, int):
                            value = [value,]
                        class_obj = Classs.objects.filter(id__in=value) 
                    else:
                        class_obj = Classs.objects.filter(name=value)
            elif request.data.get('attrid')  !=None:
                class_obj = Classs.objects.all()
            
                    
                  

            else:
                class_obj = Classs.objects.all()
              
                #gg = self.adding(class_obj,request.data.get('page'))
                
                if request.data.get('page')==None:
                    page =1
                else:
                    page = int(request.data.get('page'))
                paginator = Paginator(class_obj,2)
                try:
                    
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                class_numpages = paginator.num_pages
                pagination_obj = self.pagination_data(class_numpages,users,page)

                
                

            if request.data.get('id')!= None:
                serializer_obj = serializers.ClasssSerializer(class_obj,many=True) 
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
                
            elif request.data.get('conditions')  !=None:
                # condition = request.data.get('conditions') 

                # condition = json.loads(condition)
                # value = condition["id"]
                # class_obj = Classs.objects.filter(id=value)
                serializer_obj=  serializers.ClasssSerializer(class_obj,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            elif request.data.get('attrid')  !=None:
                serializer_obj = serializers.ClasssSerializer(class_obj,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error}


            else:
                serializer_obj = serializers.ClasssSerializer(users,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error,"paginations":pagination_obj}
            
        elif request.data.get('action') =='Update':

            class_objs = Classs.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],
            order=request.data['order'],description=request.data['description']
            )
            serializer_obj = serializers.ClasssSerializer(Classs.objects.filter(id=request.data['id']),many=True)
            data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            
        
        elif request.data.get('action') =='remove':
            instance = Classs.objects.get(id=request.data.get('id'))
            instance.delete()
            data= {"data":request.data,"status": True,"errors":data_error}

        #serializer = serializers.ClasssSerializer(class_obj)
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = serializers.ClasssSerializer(data=request.data)
        data_error = []
        if serializer.is_valid:
            Classs.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],created_on=request.data['created_on'],
                order=request.data['order'],description=request.data['description'],
                created_by=int(request.data['created_by']))
            serializer_obj=  serializers.ClasssSerializer(Classs.objects.filter(id=pk),many=True)
            data= {"data":serializer_obj.data,"status": True,"errors":data_error}
        else:
            for keys in request.data.items():
                if bool(request.data[keys]) == False:
                    data_error.append(keys + " Can Not be Blank")
            data = {"data": request.data,"status": False,"errors": data_error}
            
        return Response(data,status=status.HTTP_200_OK)

    def update(self, request, pk=None):   
        try:
            class_objs = Classs.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],created_on=request.data['created_on'],
            order=request.data['order'],description=request.data['description'],
            created_by=int(request.data['created_by']))
           
        except:
            pass
        # class_obj = Classs.objects.all()
        # serializer = serializers.ClasssSerializer(class_obj,many=True)        
        return Response({"serializer.data":"ddsds"})    

    def destroy(self, request, pk=None):
        try:
            instance = Classs.objects.get(id=pk)
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgramsViewset(viewsets.ModelViewSet):
    queryset = Programs.objects.all()
    serializer_class = serializers.ProgramsSerializer

    def create(self, request, *args, **kwargs): 
        
        
        data_error = []
        #t##ry: 
        if request.data.get('action') =='add':
            

            program_obj = Programs.objects.create(name=request.data['name'],
            display_name=request.data['display_name'],
            description=request.data['description'],
            )
            serializer_obj = serializers.ProgramsSerializer(Programs.objects.filter(id=program_obj.id),many=True)
            data= {"data":serializer_obj.data,"status": True,"errors":data_error}
        elif request.data.get('action') =='view':
            if request.data.get('id')!= None:
                program_obj = Programs.objects.filter(id=request.data.get('id'))  
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    program_obj = Programs.objects.filter(id=conditionn[key])  
            elif request.data.get('idr')  !=None:
                    
                    program_obj = Programs.objects.all()
                    # serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True)
                    
                    # data= {"data":serializer_obj.data,"status": True,"errors":data_error}                
            else:
                program_obj = Programs.objects.all()
                program_data = program_obj.values()
                if request.data.get('page')==None:
                    page =1
                else:
                    page = int(request.data.get('page'))
                paginator = Paginator(program_obj,2)
                try:
                    
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                

                if program_numpages > 0:
                    program_numpage =  program_numpages
                    
                    
                    #batch_range = "paginator.page_range"
                    program_next = users.has_next()
                    
                    
                    program_previous = users.has_previous()
                    program_user_changes = users.has_other_pages()
                   

                    if program_next == True:
                        program_next_page_number = users.next_page_number()
                        
                    
                    if page >1:
                        program_previous_page = users.previous_page_number()
                        current_page = users.number
                    else:
                        program_previous_page = 1
                        current_page = 1
                    #print(current_page)
                    program_index = users.start_index()
                    program_end = users.end_index()
                    if program_next != True:
                        program_record ={"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_previous_page":program_previous_page,"program_index":program_index,"program_end":program_end,"current_page":current_page}
                        
                        
                        
                    else:
                        program_next_page_number = users.next_page_number()
                        
                        program_record = {"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_previous_page":program_previous_page,"program_index":program_index,"program_end":program_end,"current_page":current_page,"class_next_page_number":program_next_page_number}

                
                    
                else:
                    class_record = {"class_numpage":class_numpages}
            
            if request.data.get('id')!= None:
                serializer_obj = serializers.ProgramsSerializer(program_obj,many=True) 
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
                
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    class_obj = Programs.objects.filter(id=conditionn[key])
                    serializer_obj = serializers.ProgramsSerializer(Programs,many=True)
                    data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            elif request.data.get('idr')  !=None:
                    
                    program_obj = Programs.objects.all()
                    serializer_obj = serializers.ProgramsSerializer(program_obj,many=True) 
                    data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
            else:
                serializer_obj = serializers.ProgramsSerializer(users,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error,"paginations":program_record}






            # serializer_obj = serializers.ProgramsSerializer(program_obj,many=True)
            # data= {"data":serializer_obj.data,"status": True,"errors":data_error}
        elif request.data.get('action') =='Update':
            program_obj = Programs.objects.filter(id=int(request.data['id'])).update(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'])
            serializer_obj = serializers.ProgramsSerializer(Programs.objects.filter(id=request.data['id']),many=True)
            data= {"data":serializer_obj.data,"status": True,"errors":data_error}
        elif request.data.get('action') =='remove':
            instance = Programs.objects.get(id=int(request.data['id']))
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
       

        return Response(data,status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        program = request.data
        data_error = []
        for keys in request.data.items():
                if bool(request.data[keys]) == False:
                    data_error.append(keys + " Can Not be Blank")
        try:
            if len(data_error) == 0: 
                program_obj = Programs.objects.filter(id=request.data['id']).update(name=program['name'],display_name=program['display_name'],description=program['description'],type=program['type'])
                
                serializer_obj = serializers.ProgramsSerializer(Programs.objects.filter(id=request.data['id']),many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
            else:
                data = {"data": request.data,"status": False,"errors": data_error}      
        except:
            
            data = {"data": request.data,"status": False,"errors": data_error}   

        return Response(data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        try:
            instance = Programs.objects.get(id=pk)
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

#################Programhasclasses################

class ProgramhasclassesViewset(viewsets.ModelViewSet):
    queryset = Programhasclasses.objects.all()
    serializer_class = serializers.ProgramhasclassesSerializer
    #filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    filterset_fields = ['program_class']

    def create(self, request):
        data_error = []
        # # for keys,value in request.data.items():
        # #         if bool(request.data[keys]) == False:
        #             data_error.append(keys + " Can Not be Blank")
        try:
            if request.data.get('action') =='add':
                if len(data_error) == 0: 
                    
                    
                    program_class_obj = Programhasclasses.objects.create(class_id=Classs.objects.get(id=request.data['class_id']),program=Programs.objects.get(id=request.data['program']),created_by=int(request.data['created_by']))
                    serializer_obj = serializers.ProgramhasclassesSerializer(Programhasclasses.objects.filter(id=program_class_obj.id),many=True) 
                    data = {"data":serializer_obj.data,"status": True,"errors":data_error} 
                else:
                    data = {"data": request.data,"status": False,"errors": data_error}  
            elif request.data.get('action') =='view':
                if request.data.get('id')!= None:
                    program_obj = Programhasclasses.objects.filter(id=request.data.get('id'))                    
                else:
                    program_obj = Programhasclasses.objects.all()
                    program_data = program_obj.values()
                serializer_obj = serializers.ProgramhasclassesSerializer(program_obj,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
            elif request.data.get('action') =='Update':
                if request.data.get('id')!= None:   
                     if len(data_error) == 0: 
                        try:          
                            program_obj = Programhasclasses.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],class_id=Classs.objects.get(id=request.data['class_id']),created_by=int(request.data['created_by']),program=Programs.objects.get(id=request.data['program']))
                            serializer_obj = serializers.ProgramhasclassesSerializer(Programhasclasses.objects.filter(id=request.data['id']),many=True)   
                            data = {"data":serializer_obj.data,"status": True,"errors":data_error} 
                        except:
                            data = {"data": request.data,"status": False,"errors": data_error}

                if len(data_error) == 0:
                    
                    program_class_obj = Programhasclasses.objects.create(created_on=request.data['created_on'],class_id=Classs.objects.get(id=request.data['class_id']),program=Programs.objects.get(id=request.data['program']),created_by=int(request.data['created_by']))
                    
                    serializer_obj = serializers.ProgramhasclassesSerializer(Programhasclasses.objects.filter(id=program_class_obj.id),many=True) 
                    data = {"data":serializer_obj.data,"status": True,"errors":data_error} 
                else:
                    data = {"data": request.data,"status": False,"errors": data_error} 
                    ######################View############################## 
            elif request.data.get('action') =='view':
                if request.data.get('id')!= None:
                    program_has_class = Programhasclasses.objects.filter(id=request.data.get('id'))  
                else:
                    program_has_class = Programhasclasses.objects.all() 
                serializer_obj = serializers.ProgramhasclassesSerializer(program_has_class,many=True)
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}
            elif request.data.get('action') =='Update':
                
                if len(data_error) == 0: 
                    try:
                        if request.data.get('id')!= None:          
                            program_obj = Programhasclasses.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],class_id=Classs.objects.get(id=request.data['class_id']),created_by=int(request.data['created_by']),program=Programs.objects.get(id=request.data['program']))
                            serializer_obj = serializers.ProgramhasclassesSerializer(Programhasclasses.objects.filter(id=request.data['id']),many=True)   
                            data = {"data":serializer_obj.data,"status": True,"errors":data_error} 
                        else:
                            data = {"data": request.data,"status": False,"errors": data_error} 
                    except:
                        data = {"data": request.data,"status": False,"errors": data_error} 

                else:
                    data = {"data": request.data,"status": False,"errors": data_error} 
            elif request.data.get('action') =='remove':
                try:
                    instance = Programhasclasses.objects.get(id=request.data.get('id'))
                    instance.delete()
                    class_obj = Classs.objects.filter(id=request.data.get('id')).count()
                    if class_obj !=0:
                        serializer_obj=  serializers.ClasssSerializer(Classs.objects.filter(id=request.data.get('id')),many=True)
                    else:
                        serializer_obj=  serializers.ClasssSerializer(Classs.objects.all(),many=True)

                    #serializer_obj=  serializers.ClasssSerializer(Classs.objects.all(),many=True)
                    data= {"data":"Its deleted Successfully","status": True,"errors":data_error} 
                except:
                    data= {"data":"Its Invalid Id","status": True,"errors":data_error}

        except:
            
            data = {"data": request.data,"status": False,"errors": data_error}  
        return Response(data, status=status.HTTP_200_OK)

    

   

    def update(self,request,*args, **kwargs):
        program_has_class = request.data
        data_error = []
        for keys in request.data.items():
                if bool(request.data[keys]) == False:
                    data_error.append(keys + " Can Not be Blank")
        if len(data_error) == 0: 
            try:          
                program_obj = Programhasclasses.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],class_id=Classs.objects.get(id=request.data['class_id']),created_by=int(request.data['created_by']),program=Programs.objects.get(id=request.data['program']))
                serializer_obj = serializers.ProgramhasclassesSerializer(Programhasclasses.objects.filter(id=request.data['id']),many=True)   
                data = {"data":serializer_obj.data,"status": True,"errors":data_error} 
            except:
                data = {"data": request.data,"status": False,"errors": data_error} 

        else:
            data = {"data": request.data,"status": False,"errors": data_error}      
          
        return Response(data, status=status.HTTP_200_OK)
        # return Response(serializer.data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        try:
            instance = Programhasclasses.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProgramclasshassubjectsViewset(viewsets.ModelViewSet):
    queryset = Programclasshassubjects.objects.all()
    serializer_class = serializers.ProgramclasshassubjectsSerializer

    def create(self,request):
        has_subjects = request.data
        data_error = []
             
        try:
            if request.data.get('action') =='add':
                if len(data_error) == 0: 
                    
                    prog_sub_class = Programclasshassubjects.objects.create(created_on=request.data['created_on'],program_has_class=Programhasclasses.objects.get(id=request.data['program_has_class']),created_by=int(request.data['created_by']),class_has_subjects_id=request.data['class_has_subjects_id'])
                    serializer_obj = serializers.ProgramclasshassubjectsSerializer(Programclasshassubjects.objects.filter(id=prog_sub_class.id),many=True)  
                    data = {"data": "serializer_obj.data","status": True,"errors": data_error}
                else:      
                    data = {"data": request.data,"status": False,"errors": data_error}  
        except:
            data = {"data": request.data,"status": False,"errors": data_error} 


        return Response(data,status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        program_has_class = request.data
        has_subjects = request.data
        program_obj = Programhasclasses.objects.get(id=has_subjects['program_has_class'])
        user_obj = User.objects.get(id=has_subjects['created_by'])
        data_error = []
        for keys in request.data.items():
                if bool(request.data[keys]) == False:
                    data_error.append(keys + " Can Not be Blank")
        try:
            if len(data_error)==0:
                program_obj = Programclasshassubjects.objects.filter(id=request.data['id']).update(created_on=has_subjects['created_on'],program_has_class=program_obj,created_by=user_obj,class_has_subjects_id=has_subjects['class_has_subjects_id'])
                serializer_obj = serializers.ProgramclasshassubjectsSerializer(Programclasshassubjects.objects.filter(id=request.data['id']),many=True)  
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}  
            else:
                data = {"data": request.data,"status": False,"errors": data_error} 
        except:
            data = {"data": request.data,"status": False,"errors": data_error} 

        return Response(data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        try:
            instance = Programhasclasses.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

#####################################Sessions///////////////////
class SessionsViewset(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = serializers.SessionsSerializer

    def create(self,request):
        #has_subjects = request.data

       
        data_error = []
       
        if request.data.get('action') =='add': 
            #if len(data_error) == 0:  
                
        #created_by = request.data['created_by']
            # print(Programs.objects.get(id=request.data['program']))
            session = Sessions.objects.get_or_create(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],year=request.data['year'],
            program=Programs.objects.get(id=request.data['program']))
            serializer_obj = serializers.SessionsSerializer(Sessions.objects.all(),many=True)  
            data = {"data": serializer_obj.data,"status": True,"errors": data_error} 
            # else:
            #      data = {"data": request.data,"status": True,"errors": data_error}  
        elif request.data.get('action') =='view': 
            if request.data.get('id')!= None:  
                session_obj = Sessions.objects.filter(id=request.data.get('id'))
            elif request.data.get('identr')  !=None:
                session_obj = Sessions.objects.all()
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    session_obj = Sessions.objects.filter(id=conditionn[key])
            else:
                session_obj = Sessions.objects.all()    
            
                if request.data.get('page')==None:
                        page =1
                else:
                    page = int(request.data.get('page'))         
                paginator = Paginator(session_obj,2)
                try:
                    
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                
                session_numpages = paginator.num_pages
                if session_numpages > 0:
                    session_numpage =  session_numpages
                    session_next = users.has_next()
                    session_previous = users.has_previous()
                    session_user_changes = users.has_other_pages()
                    if page >1:
                        session_previous_page = users.previous_page_number()
                    
                        current_page = users.number
                    else:
                        session_previous_page = 1
                        current_page = 1
                   
                    session_index = users.start_index()
                    session_end = users.end_index()
                    if session_next == True:
                        session_next_page_number = users.next_page_number()
                        session_ob = {"session_numpage":session_numpage,"session_next":session_next,
                        "session_previous":session_previous,"session_user_changes":session_user_changes,
                        "session_previous_page":session_previous_page,"batch_index":session_index,"session_end":session_end,"current_page":current_page,"session_next_page_number":session_next_page_number}
                    else:
                        session_ob = {"session_numpage":session_numpage,"session_next":session_next,
                        "session_previous":session_previous,"session_user_changes":session_user_changes,
                        "session_previous_page":session_previous_page,"batch_index":session_index,"session_end":session_end,"current_page":current_page}
                else:
                    
                    class_record = {"session_numpages":session_numpages}
            if request.data.get('id')!= None:
                serializer_obj = serializers.SessionsSerializer(session_obj,many=True) 
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
            elif request.data.get('identr')  !=None:
                session_obj = Sessions.objects.all()
                serializer_obj = serializers.SessionsSerializer(session_obj,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error}
                
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    class_obj = Sessions.objects.filter(id=conditionn[key])
                    serializer_obj = serializers.SessionsSerializer(session_obj,many=True)
                    data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            else:
                serializer_obj = serializers.SessionsSerializer(users,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error,"paginations":session_ob}

        elif request.data.get('action') =='Update': 
            #print("@@@@@@@@@@@",request.data['id'])
            session_obj = Sessions.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],year=request.data['year'],
            program=Programs.objects.get(id=request.data['program']))
            serializer_obj = serializers.SessionsSerializer(Sessions.objects.filter(id=request.data['id']),many=True) 
            data = {"data": "serializer_obj.data","status": True,"errors": data_error}
        elif request.data.get('action') =='remove': 
            instance = Sessions.objects.get(id=request.data['id'])
            instance.delete()
            session_count = Sessions.objects.filter(id=request.data['id']).count()
            if session_count >0:
                session = Sessions.objects.filter(id=request.data['id'])   

                serializer_obj = serializers.SessionsSerializer(session,many=True)
            else:
                serializer_obj = request.data
            data = {"data": serializer_obj.data,"status": True,"errors": data_error}
        # else:
        #     data = {"data": request.data,"status": False,"errors": data_error} 
        return Response(data,status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        program_has_class = request.data
        has_subjects = request.data
        data_error = []
        for keys in request.data.items():
            if bool(request.data[keys]) == False:
                data_error.append(keys + " Can Not be Blank")
        if len(data_error) == 0:        
            session_obj = Sessions.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],created_by=request.data['created_by'],name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],year=request.data['year'],
                program=Programs.objects.get(id=request.data['program']))
            serializer_obj = serializers.SessionsSerializer(Sessions.objects.filter(id=request.data['id']),many=True) 
            data = {"data": serializer_obj.data,"status": True,"errors": data_error}       
        else:
            data = {"data": request.data,"status": False,"errors": data_error} 
        return Response(data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        try:
            instance = Sessions.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)




###############################PhaseHasSession######################

class PhaseHasSessionViewset(viewsets.ModelViewSet):
    queryset = PhaseHasSession.objects.all()
    serializer_class = serializers.PhaseHasSessionSerializer

    def create(self,request):
       
        data_error = []
        # for keys in request.data.items():
        #         if bool(request.data[keys]) == False:
        #             data_error.append(keys + " Can Not be Blank")
        #try:
            
            
        if request.data.get('action') =='add':
            # for keys in request.data.items():
            #     print(bool(request.data[keys]))
                # if bool(request.data[keys]) == False:
                #     print("hhh")
                    # data_error.append(keys + " Can Not be Blank")
            if len(data_error) ==0:

            #has_subjects['created_by'] = User.objects.get(id=request.data['created_by'])
                
                phase_session = PhaseHasSession.objects.get_or_create(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],start_date=request.data['start_date'],
                end_date=request.data['end_date'],session=Sessions.objects.get(id=request.data['session']))
                serializer_obj = serializers.PhaseHasSessionSerializer(PhaseHasSession.objects.all(),many=True) 
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}
            else:
                    data = {"data": request.data,"status": True,"errors": data_error}
        elif request.data.get('action') =='view':  
            if request.data.get('id')!= None:
                
                phase_session = PhaseHasSession.objects.filter(id=request.data.get('id')) 
            elif request.data.get('idr')  !=None:
                    
                    phase_session = PhaseHasSession.objects.all()
                    serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True)

            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    phase_session = PhaseHasSession.objects.filter(id=value)                    
            else:
                phase_session = PhaseHasSession.objects.all()
                #-----------------------------------------------------
                if request.data.get('page')==None:
                    page =1
                else:
                    page = int(request.data.get('page'))
                
                paginator = Paginator(phase_session,2)
                try:
                    
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                class_numpages = paginator.num_pages
                

                if class_numpages > 0:
                    class_numpage =  class_numpages
                    
                    
                    #batch_range = "paginator.page_range"
                    class_next = users.has_next()
                    
                    
                    class_previous = users.has_previous()
                    class_user_changes = users.has_other_pages()
                

                    if class_next == True:
                        class_next_page_number = users.next_page_number()
                        
                    
                    if page >1:
                        class_previous_page = users.previous_page_number()
                        current_page = users.number
                    else:
                        class_previous_page = 1
                        current_page = 1
                    #print(current_page)
                    class_index = users.start_index()
                    class_end = users.end_index()
                    if class_next != True:
                        
                        
                        class_record = {"class_numpage":class_numpages,"class_next":class_next,
                        "class_previous":class_previous,"class_user_changes":class_user_changes,
                        "class_previous_page":class_previous_page,"class_index":class_index,"class_end":class_end,"current_page":current_page}
                    else:
                        class_next_page_number = users.next_page_number()
                        class_record = {"class_numpage":class_numpages,"class_next":class_next,
                        "class_previous":class_previous,"class_user_changes":class_user_changes,
                        "class_previous_page":class_previous_page,"class_index":class_index,"class_end":class_end,"current_page":current_page,"class_next_page_number":class_next_page_number}
                    
                else:
                    class_record = {"class_numpage":class_numpages}
            if request.data.get('id')!= None:
                serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True) 
                
                data= {"data":serializer_obj.data,"status": True,"errors":data_error} 
            elif request.data.get('conditions')  !=None:
                    serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True)
                    
                    data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            elif request.data.get('idr')  !=None:
                    
                    phase_session = PhaseHasSession.objects.all()
                    serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True)
                    
                    data= {"data":serializer_obj.data,"status": True,"errors":data_error}
            else:
                serializer_obj = serializers.PhaseHasSessionSerializer(users,many=True)
                data= {"data":serializer_obj.data,"status": True,"errors":data_error,"paginations":class_record}
                
            

        




                ############################################################
            # serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True)
            # data = {"data": serializer_obj.data,"status": True,"errors": data_error}
        elif request.data.get('action') =='remove':  
            if request.data.get('id')!= None:
                instance = PhaseHasSession.objects.get(id=request.data.get('id'))
                instance.delete()
                phase_session = PhaseHasSession.objects.all() 
                serializer_obj = serializers.PhaseHasSessionSerializer(phase_session,many=True) 
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}
        elif request.data.get('action') =='Update':
            if len(data_error) ==0:
                
                # created_by = request.data['created_by']
                program_obj = PhaseHasSession.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],start_date=request.data['start_date'],
                end_date=request.data['end_date'],session=Sessions.objects.get(id=request.data['session']))
                serializer_obj = serializers.PhaseHasSessionSerializer(PhaseHasSession.objects.filter(id=request.data['id']),many=True)        
                #data = {"data": serializer_obj.data,"status": True,"errors": data_error}   
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}    

            else:
                
                data = {"data": request.data,"status": False,"errors": data_error} 
        
        

        return Response(data,status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = PhaseHasSession.objects.all()
        serializer = serializers.PhaseHasSessionSerializer(queryset,many=True)
        
        return super().list(request, *args, **kwargs)

    

    # def get_queryset(self, *args, **kwargs):
    #     return (self.request)

    def update(self, request, *args, **kwargs):
        has_subjects = request.data
        created_on = request.data['created_on']
        name = request.data['name']
        data_error = []
        for keys in request.data.items():
                if bool(request.data[keys]) == False:
                    data_error.append(keys + " Can Not be Blank")
        try:
            if len(data_error) ==0:
                created_by = User.objects.get(id=request.data['created_by'])
                program_obj = PhaseHasSession.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],created_by=created_by,name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],start_date=request.data['start_date'],
                    end_date=request.data['end_date'],session=Sessions.objects.get(id=request.data['session']))
                serializer = serializers.PhaseHasSessionSerializer(PhaseHasSession.objects.filter(id=request.data['id']),many=True)        
                data = {"data": serializer_obj.data,"status": True,"errors": data_error}       
            else:
                data = {"data": request.data,"status": False,"errors": data_error} 
        
        except:

            data = {"data": request.data,"status": False,"errors": data_error} 

        return Response(data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        try:
            instance = PhaseHasSession.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

################Batch#################

# class BatchessViewApiView(APIView):
#     def post(self, request, *args, **kwargs):
#         return Response({"status":"status"}
class BatchesView(viewsets.ModelViewSet):
    queryset = Batches.objects.all()
    serializer_class = serializers.BatchesSerializer

    def create(self,request):

        data_error = []
        #try: 
        if request.data.get('action') =='add': 
            print(request.data)
            
            #user_obj = request.data['created_by']    
            if request.data['end_date'] !='':
                endi = request.data['end_date'].split("/")
                end_date = endi[2]+"-"+endi[0]+"-"+endi[1]
            else:
                end_date = request.data['end_date']

            if request.data['start_date'] !='':
                start = request.data['start_date'].split("/")
                start_date = start[2]+"-"+start[0]+"-"+start[1]
            else:
                start_date = request.data['start_date']
                
            
            batches = Batches.objects.get_or_create(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],start_date=start_date,
            end_date=end_date,phase=PhaseHasSession.objects.get(id=request.data['phase']),times_slot=request.data['times_slot'])
            serializer_obj = serializers.BatchesSerializer(Batches.objects.all(),many=True) 
            
            data = {"data": serializer_obj.data,"status": True,"errors": data_error}       
            # return Response(data,status=status.HTTP_200_OK)
        elif request.data.get('action') =='view':
            if request.data.get('id')!= None:
                batches_obj = Batches.objects.filter(id=request.data.get('id'))
            
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    batches_obj = Batches.objects.filter(id=conditionn[key])
                    
                    
                      
            else:
                batches_obj = Batches.objects.all()
                if request.data.get('page')==None:
                    page =1
                else:
                    page = int(request.data.get('page'))
                
                
                
                paginator = Paginator(batches_obj,2)
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

                    if batch_next == True:
                        class_next_page_number = users.next_page_number()
                        batches_ob = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                        "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                        "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page,"class_next_page_number":class_next_page_number}
                    else:
                        batches_ob = {"batch_numpage":batch_numpage,"batch_next":batch_next,
                        "batch_previous":batch_previous,"batch_user_changes":batch_user_changes,
                        "batch_previous_page":batch_previous_page,"batch_index":batch_index,"batch_end":batch_end,"current_page":current_page}
                    #print(batchee)

                else:
                    batches_ob = {"batch_numpage":batch_numpages}



                #print({ 'users': users })
            
            if request.data.get('id')!= None:
                serializer_obj = serializers.BatchesSerializer(batches_obj,many=True) 
                data = {"data": serializer_obj.data,"errors": data_error,"status": True}
            elif request.data.get('conditions')  !=None:
                condition = request.data.get('conditions') 
                conditionn = json.loads(condition) 
                for key,value in conditionn.items(): 
                    batches_obj = Batches.objects.filter(id=conditionn[key]) 
                    serializer_obj = serializers.BatchesSerializer(batches_obj,many=True)
                    data = {"data": serializer_obj.data,"errors": data_error,"status": True}
            else:
                serializer_obj = serializers.BatchesSerializer(users,many=True)
                data = {"data": serializer_obj.data,"errors": data_error,"status": True,"paginations":batches_ob}

        elif request.data.get('action') =='Update':
            
            if request.data.get('id')!= None:
                if request.data['end_date'] !='':
                    endi = request.data['end_date'].split("/")
                    end_date = endi[2]+"-"+endi[0]+"-"+endi[1]
                else:
                    end_date = request.data['end_date']

                if request.data['start_date'] !='':
                    start = request.data['start_date'].split("/")
                    start_date = start[2]+"-"+start[0]+"-"+start[1]
                else:
                    start_date = request.data['start_date']
                
                program_obj = Batches.objects.filter(id=request.data['id']).update(name=request.data['name'],display_name=request.data['display_name'],description=request.data['description'],start_date=start_date,
                end_date=end_date,phase=PhaseHasSession.objects.get(id=request.data['phase']))
                serializer_obj = serializers.BatchesSerializer(Batches.objects.filter(id=request.data['id']),many=True)  
                data = {"data": serializer_obj.data,"errors": data_error,"status": True}

        elif request.data.get('action') =='remove':
            instance = Batches.objects.get(id=request.data['id'])
            instance.delete()
            data = {"data": "serializer_obj.data","errors": data_error,"status": True}
        return Response(data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = Batches.objects.all()
        serializer = serializers.BatchesSerializer(queryset,many=True)
        
        return Response(serializer.data)

    def update(self,request,*args, **kwargs):

        has_subjects = request.data
        has_subjects['created_on'] = request.data['created_on']
        has_subjects['name'] = request.data['name']
        has_subjects['created_by'] = User.objects.get(id=has_subjects['created_by'])
        program_obj = Batches.objects.filter(id=request.data['id']).update(created_on=has_subjects['created_on'],created_by=has_subjects['created_by'],name=has_subjects['name'],display_name=has_subjects['display_name'],description=has_subjects['description'],start_date=has_subjects['start_date'],
            end_date=request.data['end_date'],phase=PhaseHasSession.objects.get(id=request.data['phase']))
        serializer = serializers.BatchesSerializer(Batches.objects.filter(id=request.data['id']),many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        try:
            instance = Batches.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


#################################################SudentClassPath##########################


class StudentClassPathView(viewsets.ModelViewSet):
    queryset = StudentClassPath.objects.all()
    serializer_class = serializers.SudentClassPathSerializer

    def create(self,request):
        user_obj = User.objects.get(id=request.data['created_by'])
        data= {}
        data_error = []
        for keys,value in request.data.items():
            if bool(request.data[keys]) == False:
                data_error.append(keys + " Field Can Not be Blank")
        
        
        if len(data_error) ==0:
            serializer = serializers.SudentClassPathSerializer(data=request.data)
            if serializer.is_valid:
                user_obj = User.objects.get(id=request.data['created_by'])
                student_cl_path = StudentClassPath.objects.create(created_on=request.data['created_on'],created_by=user_obj,student_id=request.data['student_id'],current=request.data['current'],classes=Classs.objects.get(id=request.data['classes']))
                serializerss = serializers.SudentClassPathSerializer(StudentClassPath.objects.get(id=student_cl_path.id))
                data = {"data":serializerss.data,"status": True}
                data['errors']={}
            else:
                data = {"errors": data_error}
        else:
            data = {"data": request.data,"status": False,"errors": data_error}
        return Response(data,status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self,request,*args, **kwargs):
       
        user_obj = User.objects.get(id=request.data['created_by'])
       
       
        program_obj = StudentClassPath.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],created_by=user_obj,student_id=request.data['student_id'],current=request.data['current'],classes=Classs.objects.get(id=request.data['classes']))
        serializer = serializers.SudentClassPathSerializer(StudentClassPath.objects.filter(id=request.data['id']),many=True)        
        return Response(serializer.data,status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        try:
            instance = StudentClassPath.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################FacultyHasBatchView##############################


class FacultyHasBatchView(viewsets.ModelViewSet):
    queryset = FacultyHasBatch.objects.all()
    serializer_class = serializers.FacultyHasBatchSerializer

    def create(self,request):
        user_obj = User.objects.get(id=request.data['created_by'])
        data= {}
        data_error = []
        for keys,value in request.data.items():
            if bool(request.data[keys]) == False:
                data_error.append(keys + " Can Not be vlank")
       
        if len(data_error) == 0:  
            serializer = serializers.FacultyHasBatchSerializer(data=request.data)
            if serializer.is_valid:
                user_obj = User.objects.get(id=request.data['created_by'])
                faculty_has_batch = FacultyHasBatch.objects.create(created_on=request.data['created_on'],
                created_by=user_obj,
                student_id=request.data['student_id'],faculties=request.data['faculties'],
                batches=Batches.objects.get(id=request.data['batches']))
                serializerss = serializers.FacultyHasBatchSerializer(FacultyHasBatch.objects.get(id=faculty_has_batch.id))
                data = {"data":serializerss.data,"status": True}
                data['errors']={}
            else:
                data = {"errors": data_error}
        else:
            data = {"data": request.data,"errors": data_error}
        return Response(data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self,request,*args, **kwargs):
       
        user_obj = User.objects.get(id=request.data['created_by'])   
        FacultyHasBatch.objects.filter(id=request.data['id']).update(created_on=request.data['created_on'],
                created_by=user_obj,
                student_id=request.data['student_id'],faculties=request.data['faculties'],
                batches=Batches.objects.get(id=request.data['batches']))
        serializer = serializers.FacultyHasBatchSerializer(FacultyHasBatch.objects.filter(id=request.data['id']),many=True)        
        return Response(serializer.data,status=status.HTTP_200_OK)


    def destroy(self, pk=None):
        
        try:
            instance = FacultyHasBatch.objects.get(id=pk)
            
            instance.delete()
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)