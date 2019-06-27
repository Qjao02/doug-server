class ElasticConfig():
    indexName = None
    body = None
    body_second_try = None

    def __init__(self, parameters):
        # config the index name for search
        self.indexName = 'resolucao'

        # config the search body

        for parameter in parameters['palavra_chave_resolucao']:
            simple_phrase = ' ' + parameter

        self.body = {"_source": ["*"],
                        "query": {
                            "match_phrase": {
                                "content":{
                                    "query": simple_phrase,
                                    "slop": 100
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
