
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Homeowner, Professional, UserProfile
from .forms import HomeownerSignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Professional
from django.contrib.auth import authenticate, login, logout
from .forms import HomeownerSignupForm, ProfessionalSignupForm
from .forms import HomeownerProfileForm, PhotoUploadForm
from .forms import HomeownerEditForm 
from django.contrib import messages
from .forms import PhotoUploadForm
from .forms import ProfessionalEditForm, PhotoUploadForm
from .forms import ProfessionalEditForm,ProfessionalSignupForm,PhotoUploadForm


def home(request):
    return render(request, 'home.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def resource(request):
    return render(request, 'resource.html')

def inspiration(request):
    return render(request, 'inspiration.html')

def findPro(request):
    return render(request, 'findPro.html')



def signup(request):
    if request.method == 'POST':
        form = HomeownerSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'error_message': 'Username or email already exists. Please choose a different one.'})

            # Create Homeowner profile
            homeowner = Homeowner.objects.create(user=user)

            # Log in the user
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # Redirect to the homeowner profile
            return redirect('homeowner_profile')

    else:
        form = HomeownerSignupForm()

    return render(request, 'signup.html', {'form': form, 'user_type': 'homeowner'})


def joinAsPro(request):
    form = ProfessionalSignupForm()

    if request.method == 'POST':
        form = ProfessionalSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            professional = Professional.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                bio=form.cleaned_data['bio'],
                job=form.cleaned_data['job'],
                previous_work=form.cleaned_data['previous_work']
            )

            user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
            login(request, user)

            return redirect('professional_profile')

    return render(request, 'joinAsPro.html', {'form': form, 'user_type': 'professional'})


def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # 'identifier' can be either email or username
        password = request.POST.get('password')

        # Try to authenticate with email
        user = authenticate(request, email=identifier, password=password)

        # If not authenticated with email, try with username
        if user is None:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            auth_login(request, user)  

            # Redirect to the correct profile page based on user type
            if getattr(user, 'homeowner', None):
                return redirect('homeowner_profile')
            elif getattr(user, 'professional', None):
                return redirect('professional_profile')

            else:
                error_message = 'Invalid user type.'
                return render(request, 'user_login.html', {'error_message': error_message})
        else:
            error_message = 'Invalid email or password.'
            return render(request, 'user_login.html', {'error_message': error_message})
    else:
        return render(request, 'user_login.html')



def user_profile(request):
    user = request.user

    try:
        homeowner = Homeowner.objects.get(user=user)
        return render(request, 'homeowner_profile.html', {'homeowner': homeowner})
    except Homeowner.DoesNotExist:
        # If Homeowner does not exist, check if the user is a Professional
        try:
            professional = Professional.objects.get(user=user)
            return render(request, 'professional_profile.html', {'professional': professional})
        except Professional.DoesNotExist:
            # If neither Homeowner nor Professional, show a message to register
            return render(request, 'error.html', {'message': 'You are not registered. Please register first.'})

def services(request):
    return render(request, 'services.html')

def reso1(request):
    return render(request, 'reso1.html')

def refe(request):
    return render(request, 'refe.html')
def cost (request):
    return render(request, 'cost.html')


def tips(request):
    return render(request, 'tips.html')

def classic(request):
    return render(request, 'classic.html')
def Scandinavian(request):
    logout(request)
    return render(request,'Scandinavian.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def logout_view(request):
    logout(request)
    return render(request,'home.html')


@login_required
def homeowner_profile(request):
    user = request.user
    homeowner = Homeowner.objects.get(user=user)  

    if request.method == 'POST':
        # Handle editing profile information
        profile_form = HomeownerProfileForm(request.POST, instance=homeowner)
        if profile_form.is_valid():
            profile_form.save()

        # Handle uploading/editing a profile photo
        photo_form = PhotoUploadForm(request.POST, request.FILES, instance=homeowner)
        if photo_form.is_valid():
            photo_form.save()

        return redirect('homeowner_profile')

    else:
        # For displaying the profile and handling form submissions
        profile_form = HomeownerProfileForm(instance=homeowner)
        photo_form = PhotoUploadForm(instance=homeowner)

    
    return render(request, 'homeowner_profile.html', {'homeowner': homeowner})

@login_required
def edit_profile(request):
    homeowner = Homeowner.objects.get(user=request.user)

    if request.method == 'POST':
        form = HomeownerEditForm(request.POST, instance=homeowner)
        if form.is_valid():
            form.save()
            return redirect('homeowner_profile')
    else:
        form = HomeownerEditForm(instance=homeowner)

    return render(request, 'edit_profile.html', {'form': form, 'homeowner': homeowner})


@login_required
def edit_photo(request):
    homeowner = request.user.homeowner

    if request.method == 'POST':
        photo_form = PhotoUploadForm(request.POST, request.FILES, instance=homeowner)
        if photo_form.is_valid():
            photo_form.save()
            return redirect('homeowner_profile')

    else:
        photo_form = PhotoUploadForm(instance=homeowner)

    return render(request, 'edit_photo.html', {'homeowner': homeowner, 'photo_form': photo_form})



def save_photo_changes(request):
    if request.method == 'POST':
        photo_form = PhotoUploadForm(request.POST, request.FILES)

        if photo_form.is_valid():
            # Save the changes to the user's photo
            # Example: request.user.profile.photo = photo_form.cleaned_data['photo']
            # Save the user's profile
            # request.user.profile.save()

            messages.success(request, 'Changes to the photo were saved successfully.')
        else:
            messages.error(request, 'Error saving changes to the photo. Please check the form.')

    return redirect('edit_photo')  # Redirect back to the edit_photo page after saving changes



@login_required
def professional_profile(request):
    user = request.user

    try:
        professional = Professional.objects.get(user=user)
        return render(request, 'professional_profile.html', {'professional': professional})
    except Professional.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not registered as a professional.'})


@login_required
def edit_professional_profile(request):
    professional = Professional.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfessionalEditForm(request.POST, instance=professional)
        if form.is_valid():
            form.save()
            return redirect('professional_profile')
    else:
        form = ProfessionalEditForm(instance=professional)

    return render(request, 'edit_professional_profile.html', {'form': form, 'professional': professional})



@login_required
def edit_professional_photo(request):
    professional = Professional.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=professional)
        if form.is_valid():
            form.save()
            return redirect('professional_profile')
    else:
        form = PhotoUploadForm(instance=professional)
    return render(request, 'edit_professional_photo.html', {'form': form, 'professional': professional})