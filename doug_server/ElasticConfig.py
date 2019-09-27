class ElasticConfig():
    def __init__(self):
        # config the index name for search
        self.hosts = [{
        'host': 'localhost',
        'port' : 9200
         }]

        self.resolucaoIndex = 'resolucao'
        self.eventoIndex = 'evento'

        # config the search body

    def getResolutionIndex(self):
        return self.resolucaoIndex
    
    def getEventoIndex(self):
        return self.eventoIndex

    def getResolutionQuery(self, parameters):
        
        for parameter in parameters['key_words_dict']:
            simple_phrase = ' ' + parameter
            
        resolutionQuery = {"_source": ["*"],
                        "query": {
                            "match_phrase": {
                                "content":{
                                    "query": simple_phrase,
                                    "slop": 200
                                }
                            },  
                        },
                        "highlight": {
                                "fields": {
                                    "content": {}
                                }
                            },
                        "size": 20
                    }

        return resolutionQuery


    def getEventQuery(self, params, time):

        queryTerms = []
        
        # add params to elasticsearch json query
        for param in params['eventos']:
            print(param)
            queryTerms.append({
                'match': {
                    'assunto': param
                },
            })
        
        # select the time for query, it can be past or future
        if time == 'future':
            event_date = {
                'data_evento': {
                    'gt': 'now-d'
                }
            }
        elif time == 'past':
            event_date = {
                'data_evento': {
                    'lte': 'now-d'
                }
            }


        eventQuery = {
            "_source": "*",
            "query": {
            "bool": {
                "must": queryTerms,
                "filter": [{
                        "range": event_date
                    }]
                }
            }
        }
        
        return eventQuery

    def getCheckEventValue(self, term):
        query = {
            "query" : {
                "terms" : {
                    "synonyms" : term
                }
            }
        }
        
        return query

