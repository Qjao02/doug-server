from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

#serializer





# Create your views here.






class UserViewSets(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset)

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
