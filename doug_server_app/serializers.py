from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_login')

class ProfessoresSerializers(serializers.Serializer):
    class Meta:
        model = Professor
        fields = ('nome', 'email', 'lates')


class Secretario(serializers.Serializer):
    class Meta:
        model = Secretario
        fields = ('nome', 'email')



class DepartamentoSerializer(serializers.Serializer):
    pass

class SecretariaSerialzier(serializers.Serializer):
    pass

class CursoSerializer(serializers.Serializer):
    pass


