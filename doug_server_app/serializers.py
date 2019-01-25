from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_login')

class PersonSerializer(serializers.Serializer):
    model = Person
    class Meta:
        abstract = True

class ProfessoresSerializers(serializers.Serializer):
    class Meta:
        model = Professor
        fields = ('nome', 'email', 'lates')


class Secretario(serializers.Serializer):
    class Meta:
        model = Secretario
        fields = ('nome', 'email')
