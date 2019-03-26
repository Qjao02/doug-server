from doug_server_app.views import *
from rest_framework import routers

router = routers.DefaultRouter()

#routes for  dialogflow Fulfillment
router.register('', FulfillmentViewSets, base_name='Fulfillment')


#routes for Admin operations
router.register('users', UserViewSets, base_name='user')
router.register('professores', ProfessoresViewSets, base_name='professor')
router.register('secretarios', SecretarioViewSets, base_name='secretario')
router.register('departamentos', DepartamentoViewSets, base_name='departamento')
router.register('secretarias', SecretariaViewSets, base_name='secretaria')
router.register('cursos', CursoViewSets, base_name='curso')
router.register('doug', botViewSets, base_name='doug')

router.register('boletins', BoletimViewSets, base_name='boletim')
