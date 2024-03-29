from django.urls import path
from .views import home, resource, inspiration, findPro, signup, user_login, joinAsPro, services, reso1,refe, tips, privacy_policy, terms_of_use, logout_view, professional_profile, homeowner_profile,cost,classic,edit_profile, edit_photo, save_photo_changes,edit_professional_profile, edit_professional_photo,Scandinavian,projects,add_project,project_details
from . import views
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
    path('professional_profile/<int:professional_id>/', views.professional_profile, name='professional_profile'),
    path('projects/', views.projects, name='projects'), 
    path('professional/<int:professional_id>/projects/', views.projects, name='projects'),
    path('cost/',cost, name='cost'),
    path('classic/',classic, name='classic'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('edit-photo/', edit_photo, name='edit_photo'),
    path('save-photo-changes/', save_photo_changes, name='save_photo_changes'),
    path('edit_professional_profile/', edit_professional_profile, name='edit_professional_profile'),
    path('edit_professional_photo/', edit_professional_photo, name='edit_professional_photo'),
    path('Scandinavian/', Scandinavian, name='Scandinavian'),
    path('delete_project_image/<int:image_id>/', views.delete_project_image, name='delete_project_image'),
    path('add_project/', add_project, name='add_project'),
    path('project_details/<int:project_id>/', views.project_details, name='project_details'),
    path('professional_profile/<int:professional_id>/add_comment/', views.add_comment, name='add_comment'),
    


]