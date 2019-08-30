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


    def getEventQuery(self, params):

        queryTerms = []
        for param in params['eventos']:
            print(param)
            queryTerms.append({
                'match': {
                    'assunto': param
                },
            })
        
        print('bla')
        print(queryTerms)
        
        eventQuery = {
            "_source": "*",
            "query": {
            "bool": {
                "must": queryTerms,
                "filter": [{
                        "range": {
                            "data_evento": {
                                "gt": "now"
                            }
                            
                        }
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

