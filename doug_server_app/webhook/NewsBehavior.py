from .Behavior import Behavior
import requests

# for response
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions


class NewsBehavior(Behavior):

    def toDo(self, parameters, dialogflow_request):
        url_req = "http://localhost:5000/?"
        for param in parameters['palavra-chave']:
            url_req += param + "&"

        r = requests.get(url_req[0:-1])
        print(r.text)
        urls = json.loads(r.text)['urls']
        response = self.formatNewsResponse(urls)

        self.response = DialogflowResponse(response)

    def formatNewsResponse(self, urls):
        if not urls:
            return 'Não encontrei nenhuma noticia ou boletim com essas palavras, você pode tentar uma nova combinação'

        noticias = []
        boletins = []

        noticias = urls
        for i, url in enumerate(urls):
            if url.find('boletim') > 0:
                noticias = urls[:i]
                boletins = urls[i:]
                break

        response = ''
        if not noticias:
            response += 'Não achei nenhuma noticia com essas palavras  =( \n\n'
        else:
            response += 'as noticias encontradas foram:\n\n '

            for noticia in noticias[:5]:
                response += noticia + '\n\n'
        if not boletins:

            response += 'Não achei nenhum Boletim com essas palavras =( \n\n'
        else:
            response += '\n E os boletins achados foram:\n\n '
            for boletim in boletins[:5]:
                response += boletim + '\n\n'

        return response


