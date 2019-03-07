from doug_server_app.views import *
from rest_framework import routers

router = routers.DefaultRouter()

#routes for  dialogflow Fulfillment
router.register('', FulfillmentViewSets, base_name='Fulfillment')


#routes for Admin operations
router.register('user', UserViewSets, base_name='user')
router.register('professor', ProfessoresViewSets, base_name='professor')
router.register('secretario', SecretarioViewSets, base_name='secretario')
router.register('departamento', DepartamentoViewSets, base_name='departamento')
router.register('secretaria', SecretariaViewSets, base_name='secretaria')
router.register('curso', CursoViewSet, base_name='curso')
router.register('doug', botViewSet, base_name='doug')