from django.urls import path
from .views import home, resource, inspiration, findPro, signup, user_login, joinAsPro, services, reso1, refe, tips, privacy_policy, terms_of_use, logout_view, professional_profile, homeowner_profile,cost,classic

urlpatterns = [
    path('', home, name='home'),
    path('resource/', resource, name='resource'),
    path('inspiration/', inspiration, name='inspiration'),
    path('findPro/', findPro, name='findPro'),
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),  
    path('joinAsPro/', joinAsPro, name='joinAsPro'),
    path('services/', services, name='services'),
    path('reso1/', reso1, name='reso1'),
    path('refe/', refe, name='refe'),
    path('tips/', tips, name='tips'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('terms_of_use/', terms_of_use, name='terms_of_use'),
    path('logout/', logout_view, name='logout_view'),
    path('homeowner_profile/', homeowner_profile, name='homeowner_profile'),
    path('professional_profile/', professional_profile, name='professional_profile'),
     path('cost/',cost, name='cost'),
     path('classic/',cost, name='classic'),
]
