class ElasticConfig():
    indexName = None
    body = None
    body_second_try = None

    def __init__(self, parameters):
        # config the index name for search
        self.indexName = 'resolucao'

        # config the search body
        self.body = {"_source": "*",
            "query": {
                "terms_set": {
                    "content": {
                        "terms": parameters['palavra_chave_resolucao'],
                        "minimum_should_match_script": {
                            "source": "params.num_terms"
                        }
                    }
                }
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        }

        for parameter in parameters['palavra_chave_resolucao']:
            simple_phrase = ' ' + parameter

        self.body_second_try = {"_source": "*",
                                "query": {
                                    "match_phrase": {
                                        "content": simple_phrase
                                        }
                                    },
                                    "highlight": {
                                        "fields": {
                                            "content": {}
                                        }
                                    }
                                }
