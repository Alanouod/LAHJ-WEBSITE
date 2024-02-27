from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Homeowner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, default='')

class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, default='')
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=255, null=True, blank=True)
    previous_work = models.CharField(max_length=255, null=True, blank=True)


class Order(models.Model):
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    project_description = models.TextField(default="")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Order #{self.pk} - {self.project_description[:50]}..."

class Quote(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.TextField()

    def __str__(self):
        return f"Quote #{self.pk} - {self.professional.user_profile.name}"

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.name} to {self.recipient.name}"
