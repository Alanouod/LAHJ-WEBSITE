from django.urls import path
from .views import home, resource, inspiration, findPro, signup, user_login, joinAsPro, services, reso1,refe, tips, privacy_policy, terms_of_use, logout_view, professional_profile, homeowner_profile,cost,classic,edit_profile, edit_photo, save_photo_changes,edit_professional_profile, edit_professional_photo,Scandinavian,projects,add_project,project_details , save_to_wishlist,submit_rating,wishlist_photos,view_orders,submit_order, accept_order, decline_order, accept_quote,decline_quote,get_quote_details
from . import views
from .views import view_orders

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
    path('save-to-wishlist/<int:previous_work_id>/', save_to_wishlist, name='save_to_wishlist'),
    path('wishlist/photos/', views.wishlist_photos, name='wishlist_photos'),
    path('submit_rating/', submit_rating, name='submit_rating'),
    path('submit_rating/<int:professional_id>/', views.submit_rating, name='submit_rating'),
    path('wishlist-photos/', wishlist_photos, name='wishlist_photos'),
    path('professional_profile/<int:professional_id>/submit_order/', views.submit_order, name='submit_order'),
    path('homeowner/orders/', views.view_orders, name='view_orders'),
    path('professional_profile/accept_order/<int:order_id>/', accept_order, name='accept_order'),
    path('professional_profile/decline_order/<int:order_id>/', decline_order, name='decline_order'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
    path('submit_quote/<int:order_id>/', views.submit_quote, name='submit_quote'),
    path('accept_quote/', views.accept_quote, name='accept_quote'),
    path('decline_quote/', views.decline_quote, name='decline_quote'),
    path('get_quote_details/<int:order_id>/', views.get_quote_details, name='get_quote_details'),
    path('professional_profile/<int:professional_id>/start_message/', views.start_message, name='start_message'),
    path('DM/', views.DM, name='DM'),
     path('message/<int:message_id>/', views.view_chat, name='view_chat'),
     path('reply-message/<int:partner_id>/', views.reply_message, name='reply_message'),
]


    
