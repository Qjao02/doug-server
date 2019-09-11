from .Behavior import Behavior
from doug_server.ElasticConfig import  ElasticConfig
from elasticsearch import Elasticsearch

# tratamento de dados
import numpy as np
import pandas as pd
import re

import os

# for response...
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions


class ResolutionBehavior(Behavior):
    def toDo(self, parameters, dialogflow_request):

        # Create Conection with elasticSearch and config search parameters
        elasticSearchConfig = ElasticConfig()
        elasticSearch = Elasticsearch(hosts= elasticSearchConfig.hosts)

        candidates = elasticSearch.search(index=elasticSearchConfig.getResolutionIndex(), body= elasticSearchConfig.getResolutionQuery(parameters))
#        print(candidates)

        if not (candidates['hits']['total']['value'] == 0):
            df = self.responseRanking(candidates)
            response = self.formatResponse(df)
            self.response = DialogflowResponse(response)

        else:
            self.response = DialogflowResponse(
                "infelizmente não encontrei nada, tenta ai uma nova combinação de palavras,"
                + " talvez eu tenha mais sorte na proxima")


    def extractDate(self, df):

        list_date = []
        for doc in df._source:
            try:
                list_date.append(re.search("[0-9]{2}/[0-9]{2}/20[0-9]{2}", doc['content']).group())
            except:
                try:
                    list_date.append(re.search("20[0-9]{2}", doc['content']).group())
                except:
                    list_date.append(None)

        df['date'] = pd.to_datetime(list_date)

    def responseRanking(self, candidates):
        # create a dataframe with all candidates
        df = pd.DataFrame(candidates['hits']['hits'])

        # add dates for documents
        self.extractDate(df)

        # sort documents by date (most recent)
        #df.sort_values(by='date', ascending=False, inplace=True)
        for i in range(df['_source'].shape[0]):
            text = df['_source'].loc[i]['content']
            if(re.search('SEM EFICÁCIA', text)):
                df.drop([i], inplace=True)
        df.reset_index(inplace=True)

        return df

    def formatResponse(self, df):
        try:
            response = 'Encontrei algo interessante na data de {}: \n\n *"(...)'.format(df.date[0].strftime('%d/%m/%y'))
        except:
            response = 'Encontrei algo interessante, olha só:'

        # getting the most recent doctument
        for highlight in df.highlight[0]['content']:
            response += '{}'.format(re.sub(r'\<em>|\</em>|\n', ' ', highlight))

        response += '(...)"*\n\n'

        response += 'Você pode acessar este documento por este link abaixo:\n{}{} \n\n'.format(os.environ['STATIC_HOST'],df['_source'][0]['file']['filename'])
        
        if (df['_source'].shape[0] > 1):    
            response += 'caso não seja o que procura, voce pode também acessas esses links: \n'

            for i in range(1, 6):
                try:
                    response += '{}{}\n'.format(os.environ['STATIC_HOST'], df['_source'][i]['file']['filename'])
                except:
                    pass

        return response
