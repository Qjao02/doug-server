from doug_server_app.views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('user', UserViewSets, base_name='user')
router.register('professor', ProfessoresViewSets, base_name='professor')