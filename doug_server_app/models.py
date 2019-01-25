from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Professor(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(default=None)

class Secretario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField( default=None)


class Secretaria(models.Model):
    secretario = models.OneToOneField(to=Secretario, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    telefone = PhoneNumberField()

class Departamento(models.Model):
    nome = models.CharField(max_length=30)
    contato = PhoneNumberField()
    chefe_departamento = models.OneToOneField(Professor,on_delete=None)
    corpo_docente = models.ForeignKey(Professor, related_name='professores', on_delete=models.CASCADE)


class Curso(models.Model):
    nome = models.CharField(max_length=60)
    departamento_fk = models.OneToOneField(Departamento, on_delete=None)
    secretaria_fk = models.OneToOneField(Secretaria, on_delete=None)