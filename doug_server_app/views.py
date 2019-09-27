# coding=utf-8
# django imports
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
import dialogflow_v2 as dialogflow
from django.http import HttpResponse
from django.db import connection
from .models import *

# rest API imports
from .serializers import *
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import viewsets
import re
import ast

# other imports
import json
import requests
from datetime import datetime
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions
from google.protobuf.json_format import MessageToDict

from elasticsearch import Elasticsearch
import os


#webhook impors
from .webhook.Factory import Factory
# ml imports
import pickle



# Create your views here.

'''
    ADMIN AREA
'''


class UserViewSets(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, context={'request': request}, many=True)

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


class ProfessoresViewSets(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = ProfessorSerializer


# realiza o CRUD de Secretario
class SecretarioViewSets(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretarioSerializer


# realiza o CRUD de Departamento
class DepartamentoViewSets(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = DepartamentoSerializer


# realiza o CRUD de Secretaria
class SecretariaViewSets(viewsets.ModelViewSet):
    queryset = Secretaria.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretariaSerialzier


# realiza o CRUD de Cursos
class CursoViewSets(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CursoSerializer


# realiza o CRUD de Boletim
class BoletimViewSets(viewsets.ModelViewSet):
    queryset = Boletim.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = BoletimSerializer


class EventoViewSets(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = EventoSerializer


'''
    BOT AREA
'''


class botViewSets(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        pass

    def create(self, request):
        project_id = os.environ['PROJECT_ID']

        if not request.session.exists(request.session.session_key):
            request.session.create()

        session_client = dialogflow.SessionsClient()
        session_id = request.session.session_key
        session = session_client.session_path(project_id, session_id)

        message = request.data['message']

        text_input = dialogflow.types.TextInput(
            text=message, language_code='pt-BR')

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        query_result = MessageToDict(response.query_result)
        #print(query_result.keys())
        #print(query_result['webhookPayload'])
        
        print(query_result)

        query_result = self.split_message_to_client(query_result)
        return Response({'queryResult' : query_result}, status.HTTP_200_OK)

        
    def split_message_to_client(self, query_result):
        fulfillmentMessages = []

        for element in query_result['fulfillmentMessages']:
            try:
                aux = element['text']['text'][0].split('\n')
            except:
                return query_result
            aux = [x for x in aux if len(x) > 0]            
            fulfillmentMessages = [{'text': {'text':[x] }} for x in aux]

        query_result['fulfillmentMessages'] = fulfillmentMessages
            
    

        return query_result



class FulfillmentViewSets(viewsets.ViewSet):

    def create(self, request):
        dialogflow_request = DialogflowRequest(json.dumps(request.data))
        data = request.data
        queryResult = data['queryResult']
        usersIntent = queryResult['intent']['displayName']
        parameters = queryResult['parameters']


        print(parameters)
        behavior = Factory.getBehavior(usersIntent)
        behavior.toDo(parameters, dialogflow_request)
        
        behavior.response.response_payload = {
            'slack': {
                'attachments': ["cards"],
                'text': behavior.response.dialogflow_response['fulfillmentText']
            },
        }

        responseStr = behavior.getResponse().get_final_response()

        response = ast.literal_eval(responseStr)


        response['payload'].pop('google', None)

        #print(response)
        




        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')

