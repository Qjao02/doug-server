class ElasticConfig():
    indexName = None
    body = None
    body_second_try = None
    hosts = [{
        'host': 'localhost',
        'port' : 9200
    }]

    def __init__(self, parameters):
        # config the index name for search
        self.indexName = 'resolucao'

        # config the search body

        for parameter in parameters['key_words_dict']:
            simple_phrase = ' ' + parameter

        self.body = {"_source": ["*"],
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
