from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import dialogflow

from .models import *

#serializer





# Create your views here.






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


class SecretarioViewSets(viewsets.ModelViewSet):
    queryset = Secretario.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretarioSerializer


class DepartamentoViewSets(viewsets.ModelViewSet):
    queryset =  Departamento.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = DepartamentoSerializer

class SecretariaViewSets(viewsets.ModelViewSet):
    queryset = Secretaria.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = SecretariaSerialzier

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CursoSerializer



class botViewSet(viewsets.ViewSet):
    
    def list(self, request):
        pass

    def create(self, request):


    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

