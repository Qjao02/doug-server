from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.










class Secretaria(models.Model):
    email = models.EmailField()
    telefone = PhoneNumberField()

class Secretario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    secretaria = models.OneToOneField(to=Secretaria, on_delete=models.CASCADE, related_name='secretario', null=True)


class Departamento(models.Model):
    nome = models.CharField(max_length=30)
    contato = PhoneNumberField()

class Professor(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    lates = models.URLField()
    departamento = models.ForeignKey(Departamento, related_name='corpo_docente', on_delete=models.CASCADE, null= True)
    is_chefe_departamento = models.OneToOneField(Departamento,related_name='chefe_departamento', on_delete=None, null= True)

    class Meta:
        unique_together: ['email']

    def __unicode__(self):
        return '%s: %s' % (self.nome, self.email)

class Curso(models.Model):
    nome = models.CharField(max_length=60)
    departamento_fk = models.OneToOneField(Departamento, on_delete=None)
    secretaria_fk = models.OneToOneField(Secretaria, on_delete=None)


class Disciplinas(models.Model):
    nome = models.CharField(max_length=20)
    carga_horaria = models.IntegerField()
    calendario = models.DateField()
    semestre = models.IntegerField(choices=[(1,2)])
    professor_id = models.OneToOneField(Professor,on_delete=None)


class Tutores(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(default=None)
    telefone = PhoneNumberField(null=True)
    disciplina = models.OneToOneField(to=Disciplinas,on_delete=models.SET_NULL, null=True)


class Editais(models.Model):
    nome = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    path = models.URLField()
    data = models.DateField()
    informacao_adicional = models.CharField(max_length=200)


