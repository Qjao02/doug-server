from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# custom imports
import datetime
from elasticsearch import Elasticsearch
from doug_server.ElasticConfig import ElasticConfig
import spacy
from spacy import displacy
from collections import Counter
import pt_core_news_sm

import dialogflow_v2

# os imports
import os


# Create your models here.






class Entidade(models.Model):
    nome = models.CharField(max_length=30, blank= True, null= True)

    class Meta:
        abstract = True

class Pessoa(Entidade):
    email = models.EmailField()
    nome = models.CharField(max_length= 30)

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
    lattes = models.URLField()
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

class Evento(Entidade):
    assunto = models.TextField()
    data_criado = models.DateTimeField(editable= False)
    data_evento = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.data_criado = datetime.datetime.now()   
        object = super(Evento, self).save(*args, **kwargs)

     
       
'''
    @receivers
'''

# Indexa o novo evento no momento em que um evento é criado no Banco de Dados
@receiver(post_save, sender=Evento, dispatch_uid="evento criado")
def insertEventoElasticSearch(sender, instance, created, **kwargs):
    es_config = ElasticConfig()
    es = Elasticsearch(hosts=es_config.hosts)

    newInstance = {
        'assunto': instance.assunto,
        'data_criado': instance.data_criado,
        'data_evento': instance.data_evento
    }

    res = es.index(index=es_config.getEventoIndex(), doc_type='evento', id= instance.id, body= newInstance)
    print(res)

@receiver(post_save, sender= Evento)
def updateEventoKeyWordEntities(sender, instance, created, **kwargs):
    
    assunto = instance.assunto

    # instancia o modelo de nlp
    nlp = pt_core_news_sm.load()
    doc = nlp(assunto)

    # Separação de tokens
    tokens = pre_processing(doc)
    

    # Requisição do dialogflow para obter as entities
    client = dialogflow_v2.EntityTypesClient()
    parent = client.project_agent_path(os.environ['PROJECT_ID'])
    list_entity_types_response = list(client.list_entity_types(parent))

    # cria uma nova instância com as novas entities processadas
    list_entity_types_response = list(client.list_entity_types(parent))
    entity_type = list_entity_types_response[2]

    entries = []
    entities = list(entity_type.entities)
    
    for token in tokens:
        entities.append({'value': token.lemma_, 'synonyms': [token.text]})



    #realiza o submit das entities ao dialogflow
    response = client.batch_update_entities(entity_type.name, entities)
    response.done()

    # treina o modelo do
    client = dialogflow_v2.AgentsClient()
    project_parent = client.project_path(os.environ['PROJECT_ID'])

    client.train_agent(project_parent)

def pre_processing(doc):
    tokens = [token for token in doc if not token.is_stop]
    return tokens

# chega se o termo ja foi indexado
def checkTermIndexed(tokens):
    es_config = ElasticConfig()

    tokens_result = []
    for token in tokens:
        queryBody = es_config.getCheckEventValue(token)
        response = es.search(index= t, body= evento_query_term)
        
        if(response != 1):
            tokens_result.append(token)
    
    return tokens_result
        



