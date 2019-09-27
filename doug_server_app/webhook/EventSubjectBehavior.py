from .Behavior import Behavior
import requests
from elasticsearch import Elasticsearch
from doug_server.ElasticConfig import ElasticConfig

from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions

import datetime


class EventSubjectBehavior(Behavior):

    def toDo(self, parameters, dialogflow_request):
        
        time = 'future'
        es_config = ElasticConfig()
        eventQuery = es_config.getEventQuery(parameters, time)
        
        es = Elasticsearch()


        print(eventQuery)
        res = es.search(index=es_config.getEventoIndex(), body=eventQuery)

        events = res['hits']['hits']

        # if elasticsearch query return no events, the a new query is used to search for past events
        if not events:
            time = 'past'

            eventQuery = es_config.getEventQuery(parameters, time)
            res = es.search(index=es_config.getEventoIndex(), body=eventQuery)
            events = res['hits']['hits']


        print(events)
        response = self.formatNewsResponse(events, time)
        
        

        self.response = DialogflowResponse(response)

    def formatNewsResponse(self, events, time):
        if time == 'future':
            print(time)
            if not events:
                return 'Não existem eventos com esses dados cadastrados'

            response = 'Opa, achei isso aqui \n'
            for event in events:
                response += 'na data {} :\n'.format(datetime.datetime.strptime(event['_source']['data_evento'][:10],"%Y-%m-%d").strftime("%d-%m-%Y"))
                response += '"{}" \n\n'.format(event['_source']['assunto'])

        elif time == 'past' :
            print(time)
            if not events:
                return 'Não existem eventos com esses dados cadastrados'
           

            # get the first past event
            event = {}
            event['date'] = datetime.datetime.strptime(events[0]['_source']['data_evento'][:10],"%Y-%m-%d").strftime("%d-%m-%Y")
            event['subject'] = events[0]['_source']['assunto']

            response = 'Parece que este evento já ocorreu na data {} com o assunto "{}" \n'.format(event['date'], event['subject'])

        return response


