from django.shortcuts import render, redirect
from django import forms
from .models import Homeowner
from .models import Professional
from .models import ProjectImage
from .models import PreviousWork
from .models import Comment



class HomeownerSignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
    address = forms.CharField()

class HomeownerProfileForm(forms.ModelForm):
    class Meta:
        model = Homeowner
        fields = ['phone', 'address']  

class HomeownerPhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Homeowner
        fields = ['photo']  
        widgets = {'photo': forms.FileInput(attrs={'accept': 'image/*'})} 


class HomeownerEditForm(forms.ModelForm):
    class Meta:
        model = Homeowner
        fields = ['phone', 'address'] 
 

class ProfessionalSignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
    address = forms.CharField()
    bio = forms.CharField()
    job = forms.CharField()
    previous_work = forms.FileField()


class ProfessionalEditForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['phone', 'address', 'bio']

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['photo']
        widgets = {'photo': forms.FileInput(attrs={'accept': 'image/*'})}

class ProjectPhotoUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']


class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = PreviousWork
        fields = ['project_name', 'products_used', 'location', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
