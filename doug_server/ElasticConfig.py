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

    def getResolucaoIndex(self):
        return self.resolucaoIndex
    
    def getEventoIndex(self):
        return self.eventoIndex

    def getResolucaoQUery(self, parameters):
        
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


    def getEventosQuery(self):
        eventoQuery = {}
        return eventoQuery
