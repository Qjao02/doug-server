from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.




class Entidade(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        abstract = True

class Pessoa(Entidade):
    email = models.EmailField()

    class Meta:
        abstract = True
        unique_together: ['email']


class Setor(Entidade):
    email = models.EmailField()

    class Meta():
        abstract = True
        unique_together: ['email']



class Documento(models.Model):
    titulo = models.CharField(max_length= 500, blank= True, null= True)
    data_upload = models.DateField()
    disponivel_em = models.URLField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



    class Meta():
        abstract = True


class Curso(Entidade):
    pass


class Secretaria(Setor):
    telefone = PhoneNumberField()
    curso = models.OneToOneField(to=Curso, on_delete=None, related_name= 'secretaria', null=True)

class Secretario(Pessoa):
    secretaria = models.ForeignKey(to=Secretaria, on_delete=None, related_name='secretario', null=True )

class Departamento(Setor):
    contato = PhoneNumberField()
    curso = models.ForeignKey(to= Curso, on_delete=None, related_name="departamento", null=True)

class Professor(Pessoa):
    lates = models.URLField()
    departamento = models.ForeignKey(Departamento, related_name='corpo_docente', on_delete=models.CASCADE, null= True)
    is_chefe_departamento = models.OneToOneField(Departamento,related_name='chefe_departamento', on_delete=None, null= True)

    def __unicode__(self):
        return '%s: %s' % (self.nome, self.email)




class Disciplinas(Entidade):
    carga_horaria = models.IntegerField()
    dia_da_semana = models.CharField(max_length= 300)
    semestre = models.IntegerField(choices=[(1,2)])
    ano = models.IntegerField()
    professor_id = models.OneToOneField(Professor,on_delete=None)


class Tutores(Pessoa):
    telefone = PhoneNumberField(null=True)
    disciplina = models.OneToOneField(to=Disciplinas,on_delete=models.SET_NULL, null=True)


class Edital(Documento):
    path = models.URLField()
    informacao_adicional = models.CharField(max_length=200)

class Boletim(models.Model):
    data = models.DateField()
    numero = models.IntegerField(null= True, blank= True)

class Noticia(Documento):
    corpo = models.TextField()
    boletim_fk = models.ForeignKey(on_delete= models.SET_NULL, to= Boletim, null= True)


