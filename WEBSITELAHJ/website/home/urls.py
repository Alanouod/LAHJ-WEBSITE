# home/urls.py
from django.urls import path
from . import views
from .views import home, resource, inspiration,findPro,signup,login,joinAsPro,services,reso1,refe

urlpatterns = [
    path('', views.home, name='home'),
    path('resource/', resource, name='resource'),
    path('inspiration/', inspiration, name='inspiration'),
    path('findPro/', findPro, name='findPro'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('joinAsPro/', joinAsPro, name='joinAsPro'),
    path('services/', services, name='services'),
    path('reso1/', reso1, name='reso1'),
    path('refe/', refe, name='refe'),

]

