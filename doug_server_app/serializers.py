from django.contrib.auth.models import User
from rest_framework import  serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_login')



class SecretarioSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset= Secretario.objects.all(),
            fields= ['email']
        )
    ]

    class Meta:
        model = Secretario
        fields = "__all__"


class ProfessorSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=Professor.objects.all(),
            fields=('email', 'lates')
        )
    ]

    class Meta:
        model = Professor
        fields = "__all__"

class DepartamentoSerializer(serializers.ModelSerializer):

    chefe_departamento = ProfessorSerializer()
    corpo_docente = ProfessorSerializer(many=True)

    class Meta:
        model = Departamento
        fields = ('nome', 'contato','chefe_departamento','corpo_docente')


class SecretariaSerialzier(serializers.ModelSerializer):
    secretario = SecretarioSerializer(many=True, read_only=True)

    validators = [
        UniqueTogetherValidator(
            queryset=Secretaria.objects.all(),
            fields=['email']
        )
    ]

    class Meta:
        model = Secretaria
        fields = ('email', 'telefone', 'secretario', 'curso')


class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model= Curso
        fields= ['nome']












