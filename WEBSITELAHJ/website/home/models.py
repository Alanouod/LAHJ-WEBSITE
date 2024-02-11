

from django.db import models
from django.contrib.auth.models import User

class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   

class Homeowner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField('home.ProfessionalPhoto', blank=True)

class ProfessionalPhoto(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)


class orderRequest(models.Model):
    orderRequestID = models.OneToOneField(User, on_delete=models.CASCADE) 
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE) 
    professional = models.ForeignKey(Professional, on_delete=models.SET_NULL, null=True) 
    project_description = models.TextField() 
    budget = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=20, default='pending') 

class Quote(models.Model): 
    quoteID = models.OneToOneField(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE) 
    order_request = models.ForeignKey(orderRequest, on_delete=models.CASCADE) 
    cost = models.DecimalField(max_digits=10, decimal_places=2) 
    terms = models.TextField() 
    

class Order(models.Model): 
    orderID = models.OneToOneField(User, on_delete=models.CASCADE)
    orderRequestID = models.ForeignKey(orderRequest, on_delete=models.CASCADE) 
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE) 
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE) 
    status = models.CharField(max_length=20, default='pending') 
    

class Message(models.Model): 
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE) 
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE) 
    content = models.TextField() 
    date = models.DateTimeField(auto_now_add=True) 
    
