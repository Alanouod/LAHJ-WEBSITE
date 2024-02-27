
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home, resource, inspiration, findPro, signup, user_login, joinAsPro, services, reso1, refe, tips, privacy_policy, terms_of_use, user_profile,logout_view

urlpatterns = [
    path('', home, name='home'),
    path('resource/', resource, name='resource'),
    path('inspiration/', inspiration, name='inspiration'),
    path('findPro/', findPro, name='findPro'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),  # Rename login view to user_login
    path('joinAsPro/', joinAsPro, name='joinAsPro'),
    path('services/', services, name='services'),
    path('reso1/', reso1, name='reso1'),
    path('refe/', refe, name='refe'),
    path('tips/', tips, name='tips'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-use/', terms_of_use, name='terms_of_use'),
    path('user_profile/', user_profile, name='user_profile'),
    path('logout/', logout_view, name='logout'),
    
]
