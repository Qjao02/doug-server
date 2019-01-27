from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_login')

class ProfessorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Professor
        fields = ('nome', 'email', 'lates')




class Secretario(serializers.Serializer):
    class Meta:
        model = Secretario
        fields = ('nome', 'email')



class DepartamentoSerializer(serializers.Serializer):
    class Meta:
        model = Departamento
        chefe_departamento = ProfessorSerializers()
        corpo_docente = ProfessorSerializers(many=True)

        fields = '__all__'

class SecretariaSerialzier(serializers.Serializer):
    pass

class CursoSerializer(serializers.Serializer):
    pass


