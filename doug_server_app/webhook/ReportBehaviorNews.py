from .Behavior import Behavior

# for response
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions

class ReportBehaviorNews(Behavior):

    def toDo(self, parameters, dialogflow_request):
        # geting  output context parameters
        boletim_numero = dialogflow_request.request_data['queryResult']['outputContexts'][0]['parameters']['numero']

        # search for any boletim that contains the id from request
        boletim_id = Boletim.objects.filter(numero=boletim_numero).values_list('id')

        # search for any news that match with boletim id
        querySet = Noticia.objects.filter(boletim_fk=boletim_id[0][0])
        serializer = NoticiaSerializer(querySet, many=True)
        print(serializer.data)
        response = self.formatNewsResponse(serializer.data)

        self.response = DialogflowResponse(response)

    def formatNewsResponse(self, news):
        response = ''
        for new in news:
            response += ' ' + new['titulo'] + '\n'
            response += ' ' + new['corpo'] + '\n\n'

        return response

