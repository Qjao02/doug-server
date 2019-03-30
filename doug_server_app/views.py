#django imports
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
import dialogflow_v2 as dialogflow
from django.http import HttpResponse
from .models import *

#rest API imports
from .serializers import *
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import viewsets

#other imports
import json
from datetime import  datetime
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions
#serializer





# Create your views here.

'''
    ADMIN AREA
'''
class UserViewSets(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset,context= {'request': request},many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass




class ProfessoresViewSets(viewsets.ViewSet):
    '''
    list:
    Return a list of all Professores registered on database

    create:
    create method for a new professor instance, in that case validor is called on serializer class, if data is
    valid, a new instance should be created. For invalid data request, server will return a 400 error (BAD REQUEST)

    destroy:
    Destroy method for delete a professor instance, primary key is required as a query string: example: /api/professor/2 where 2 is the id of
    Professor that will be deleted from database.
    '''

    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):

        queryset = Professor.objects.all()
        serializer = ProfessorSerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        serializer = ProfessorSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response({},status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        queryset = Professor.objects.all()
        professor = get_object_or_404(queryset, pk=pk)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data, status.HTTP_302_FOUND)


    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk):
        queryset = Professor.objects.all()
        professor = get_object_or_404(queryset, pk=pk)
        professor.delete()
        return Response('ok!', status.HTTP_200_OK)

#realiza o CRUD de Secretario
class SecretarioViewSets(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretarioSerializer

#realiza o CRUD de Departamento
class DepartamentoViewSets(viewsets.ModelViewSet):
    queryset =  Departamento.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = DepartamentoSerializer

#realiza o CRUD de Secretaria
class SecretariaViewSets(viewsets.ModelViewSet):
    queryset = Secretaria.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretariaSerialzier

#realiza o CRUD de Cursos
class CursoViewSets(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CursoSerializer

#realiza o CRUD de Boletim
class BoletimViewSets(viewsets.ModelViewSet):
    queryset= Boletim.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class= BoletimSerializer



'''
    BOT AREA
'''


class botViewSets(viewsets.ViewSet):

    permission_classes = (AllowAny,)
    def list(self, request):
        pass

    def create(self, request):

        project_id = 'doug-bot-10f69'


        if not request.session.exists(request.session.session_key):
            request.session.create()

        session_client = dialogflow.SessionsClient()
        session_id = request.session.session_key
        session = session_client.session_path(project_id, session_id)
        print('Session path: {}\n'.format(session))

        message = request.data['message']
        print('message is {}'.format(message))

        text_input = dialogflow.types.TextInput(
            text=message, language_code='pt-BR')

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)



        return Response({'message': response.query_result.fulfillment_text}, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


##WEBHOOK

class Behavior():
    response = ''
    
    def toDo(self, parameters, dialogflow_request):
        pass

    def getResponse(self):
        return self.response
        

class ReportBehavior(Behavior):
    def toDo(self, parameters, dialogflow_request):
        #search boletim with the date paramn from request
        date = datetime.strptime(parameters['date'].split('T')[0],"%Y-%m-%d")
        boletim = Boletim.objects.filter(data= date.date())

        #verifica se algum boletim foi encontrado
        if (boletim.exists()):
            #init of string response
            response = ''

            #inicia o serializer
            serializer = ''            

            if(len(boletim) > 1):
                serializer = BoletimSerializer(data= boletim, many= True)         
                response =  'encontrei, ' + serializer.data
            else:
                # build the chatbot answer based on boletim number
                serializer = BoletimSerializer(boletim, many= True)

                #create response for user
                response1 = 'encontrei: o boletim de numero  ' +  str(serializer.data[0]['numero']) + 'você quer ver as noticias ?'
                response = DialogflowResponse(response1)

                #setting-up the webhook response
                response.dialogflow_response['outputContexts'] = [
                    {
                        'name': '{}/contexts/boletins-followup'.format(dialogflow_request.get_session()),
                        'parameters': {
                            'numero': serializer.data[0]['numero']
                        },
                        'lifespanCount': 5
                    }
                ]

        else:
            #if the boletim doesn't exists then the default answer is returned
            response = DialogflowResponse('Desculpa mas eu não consegui encontrar nada nesta data =(')

        #set the response attribute on behavior class
        self.response = response

class ReportBehaviorNews(Behavior):
    def toDo(self, parameters, dialogflow_request):
        #geting  output context parameters
        boletim_numero = dialogflow_request.request_data['queryResult']['outputContexts'][0]['parameters']['numero']
        
        #search for any boletim that contains the id from request
        boletim_id = Boletim.objects.filter(numero= boletim_numero).values_list('id')

        #debugprint
        print('\n\n boletim id founded when i try to recover news with that id:\n\n')
        print('--------------------------')
        print(boletim_id[0])
        print('--------------------------')

        #search for any news that match with boletim id
        querySet = Noticia.objects.filter(boletim_fk= boletim_id[0][0])
        serializer = NoticiaSerializer(querySet, many= True)
        print(serializer.data)
        response = self.formatNewsResponse(serializer.data)

        self.response = DialogflowResponse(response)



    def formatNewsResponse(self, news):
        response = ''
        for new in news:
            response += ' ' + new['titulo'] + '\n'
            response += ' ' + new['corpo'] + '\n\n'

        return response
 

    def getResponse(self):
        return self.response

class BehaviorFactory:
    def getBeahavior(self): pass

class ReportBehaviorFactory(BehaviorFactory):

    def getReportBeahavior(self):
        print('\n\n Report behavior was called, trying to find the boletim ----- \n\n')
        return ReportBehavior()

    def getReportBehaviorNews(self):
        return ReportBehaviorNews()


class Factory:

    @staticmethod
    def getBehavior(usersIntent):
        if (usersIntent == 'boletins'):
            object = ReportBehaviorFactory().getReportBeahavior()

        elif(usersIntent == 'boletins - yes'):
            object = ReportBehaviorFactory().getReportBehaviorNews()

        return object



    

class FulfillmentViewSets(viewsets.ViewSet):

    def create(self, request):
        dialogflow_request = DialogflowRequest(json.dumps(request.data))
        data = request.data
        queryResult = data['queryResult']
        usersIntent = queryResult['intent']['displayName']
        usersAction = queryResult['action']
        parameters = queryResult['parameters']
        
        print(usersIntent)
        print(usersAction)
        print(parameters)


        behavior = Factory.getBehavior(usersIntent)
        behavior.toDo(parameters, dialogflow_request)
        behavior.response.response_payload = {
            'slack': {
                'text': behavior.response.dialogflow_response['fulfillmentText']
            }
        }
        print(behavior.getResponse())



        return HttpResponse(behavior.getResponse().get_final_response(), content_type='application/json; charset=utf-8')
        

        

        

            











