from .Behavior import Behavior

# for response
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions


class ReportBehavior(Behavior):

    def toDo(self, parameters, dialogflow_request):
        # search boletim with the date paramn from request
        date = datetime.strptime(parameters['date'].split('T')[0], "%Y-%m-%d")
        boletim = Boletim.objects.filter(data=date.date())

        # verifica se algum boletim foi encontrado
        if (boletim.exists()):
            # init of string response
            response = ''

            # inicia o serializer
            serializer = ''
            boletim_id = boletim.values_list('id')

            # getting news to recover url from "boeltim"
            querySet = Noticia.objects.filter(boletim_fk=boletim_id[0])
            noticiaSerializer = NoticiaSerializer(querySet, many=True)

            if (len(boletim) > 1):
                serializer = BoletimSerializer(data=boletim, many=True)
                response = 'encontrei, ' + serializer.data
            else:
                # build the chatbot answer based on boletim number
                serializer = BoletimSerializer(boletim, many=True)

                # create response for user
                response1 = 'encontrei o boletim de numero {}, e ele está disponivel em {} você quer ver as noticias ?'.format(
                    str(serializer.data[0]['numero']), str(noticiaSerializer.data[0]['disponivel_em']))
                response = DialogflowResponse(response1)

                # setting-up the webhook response
                response.dialogflow_response['outputContexts'] = [
                    {
                        'name': '{}/contexts/boletins-followup'.format(dialogflow_request.get_session()),
                        'parameters': {
                            'numero': serializer.data[0]['numero']
                        },
                        'lifespanCount': 5
                    }
                ]

        else:
            # if the boletim doesn't exists then the default answer is returned
            response = DialogflowResponse('Desculpa mas eu não consegui encontrar nada nesta data =(')

        # set the response attribute on behavior class
        self.response = response

