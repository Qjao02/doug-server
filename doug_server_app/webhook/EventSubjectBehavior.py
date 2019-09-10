from .Behavior import Behavior
import requests
from elasticsearch import Elasticsearch
from doug_server.ElasticConfig import ElasticConfig

from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions

import datetime


class EventSubjectBehavior(Behavior):

    def toDo(self, parameters, dialogflow_request):
        es_config = ElasticConfig()
        eventQuery = es_config.getEventQuery(parameters)
        
        es = Elasticsearch()

        print(eventQuery)
        res = es.search(index=es_config.getEventoIndex(), body=eventQuery)

        events = res['hits']['hits']
        
        print(events)
        response = self.formatNewsResponse(events)
        
        

        self.response = DialogflowResponse(response)

    def formatNewsResponse(self, events):
        if not events:
            return 'Não existem eventos com esses dados cadastrados'

        response = 'Opa, achei isso aqui \n'
        for event in events:
            response += 'na data {} :\n'.format(datetime.datetime.strptime(event['_source']['data_evento'][:10],"%Y-%m-%d").strftime("%d-%m-%Y"))
            response += '"{}" \n\n'.format(event['_source']['assunto'])

            
        return response

