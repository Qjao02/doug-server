from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest, SimpleResponse, Suggestions

class Behavior():
    response = ''

    def toDo(self, parameters, dialogflow_request):
        pass

    def getResponse(self):
        return self.response

