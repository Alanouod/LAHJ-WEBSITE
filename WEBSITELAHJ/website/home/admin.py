from django.contrib import admin
from .models import Homeowner, Professional, UserProfile,PreviousWork,Wishlist,Order,Quote,Message


admin.site.register(Homeowner)
admin.site.register(Professional)
admin.site.register(UserProfile)
admin.site.register(PreviousWork)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Message)
