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

# other imports
import json
import requests
from datetime import datetime
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions


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


class ProfessoresViewSets(viewsets.ViewSet):
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
        return Response({}, status.HTTP_400_BAD_REQUEST)

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


class FulfillmentViewSets(viewsets.ViewSet):

    def create(self, request):
        dialogflow_request = DialogflowRequest(json.dumps(request.data))
        data = request.data
        queryResult = data['queryResult']
        usersIntent = queryResult['intent']['displayName']
        parameters = queryResult['parameters']

        print(usersIntent)
        print(parameters)

        behavior = Factory.getBehavior(usersIntent)
        behavior.toDo(parameters, dialogflow_request)
        behavior.response.response_payload = {
            'slack': {
                'attachments': ["cards"],
                'text': behavior.response.dialogflow_response['fulfillmentText']
            }
        }
        print(behavior.getResponse())
        return HttpResponse(behavior.getResponse().get_final_response(), content_type='application/json; charset=utf-8')

