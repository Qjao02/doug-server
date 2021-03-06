"""doug_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings



from .router import router






urlpatterns = [

    #admin routes

    path('doug/admin/', admin.site.urls),
    path('doug/api/', include(router.urls)),
    path('doug/docs/', include_docs_urls(title='doug-api-doc')),
    path('doug/api-auth/', views.obtain_auth_token, name='auth-token')
]

urlpatterns += staticfiles_urlpatterns()
    
