# home/urls.py
from django.urls import path
from . import views
<<<<<<< Updated upstream
from .views import home, resource, inspiration,findPro,signup,login,joinAsPro,services,reso1,refe,tips
=======
from .views import home, resource, inspiration,findPro,signup,login,joinAsPro,services,reso1,refe,privacy_policy,terms_of_use
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    path('tips/', tips, name='tips'),
=======
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-use/', terms_of_use, name='terms_of_use'),

>>>>>>> Stashed changes
]

