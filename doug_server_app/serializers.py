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



class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        print(instance)
        print(ret)
        ret['departamento'] = DepartamentoSerializer(instance.departamento).data
        return ret 
    


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

class BoletimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boletim
        fields= ('data', 'numero')

class NoticiaSerializer(serializers.ModelSerializer):

    class Meta:
        model= Noticia
        fields= ['titulo', 'corpo', 'boletim_fk', 'disponivel_em']













