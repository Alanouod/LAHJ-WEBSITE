
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Homeowner, Professional, UserProfile
from .forms import HomeownerSignupForm, ProfessionalSignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import HomeownerSignupForm, ProfessionalSignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


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
        user_type = request.POST.get('user_type')

        if user_type == 'homeowner':
            form = HomeownerSignupForm(request.POST)
        elif user_type == 'professional':
            form = ProfessionalSignupForm(request.POST)
        else:
            return render(request, 'signup.html', {'error_message': 'Invalid user type.'})

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'user_type': user_type, 'error_message': 'Username or email already exists. Please choose a different one.'})

            if user_type == 'homeowner':
                # Create Homeowner profile
                homeowner = Homeowner.objects.create(user=user)
            elif user_type == 'professional':
                # Create Professional profile
                professional = Professional.objects.create(user=user)
            else:
                return render(request, 'signup.html', {'error_message': 'Invalid user type.'})

            # Log in the user
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('homeowner_profile')

    else:
        user_type = request.GET.get('user_type')
        form = HomeownerSignupForm(initial={'user_type': user_type}) if user_type == 'homeowner' else ProfessionalSignupForm(initial={'user_type': user_type})

    return render(request, 'signup.html', {'form': form, 'user_type': user_type})


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



def joinAsPro(request):
    show_page2 = False

    if request.method == 'POST':
        if 'submitPage1' in request.POST:
            form_page1 = ProfessionalSignupForm(request.POST)
            if form_page1.is_valid():
                # Handle the form submission of page1
                username = form_page1.cleaned_data['username']
                email = form_page1.cleaned_data['email']
                phone = form_page1.cleaned_data['phone']
                address = form_page1.cleaned_data['address']

                # Create a new professional object
                professional = Professional(
                    username=username,
                    email=email,
                    phone=phone,
                    address=address
                )
                professional.save()

                # Set show_page2 to True to display the second page
                show_page2 = True
        elif 'submitPage2' in request.POST:
            form_page2 = ProfessionalSignupForm(request.POST)
            if form_page2.is_valid():
                # Handle the form submission of page2
                bio = form_page2.cleaned_data['bio']
                job = form_page2.cleaned_data['job']
                previous_work = form_page2.cleaned_data['previous_work']

                # Update the existing professional object with page2 data
                professional = Professional.objects.latest('id')
                professional.bio = bio
                professional.job = job
                professional.previous_work = previous_work
                professional.save()

                return redirect('user_profile')

    return render(request, 'joinAsPro.html', {'show_page2': show_page2})

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

    try:
        homeowner = Homeowner.objects.get(user=user)
        return render(request, 'homeowner_profile.html', {'homeowner': homeowner})
    except Homeowner.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not registered as a homeowner.'})

@login_required
def professional_profile(request):
    user = request.user

    try:
        professional = Professional.objects.get(user=user)
        return render(request, 'professional_profile.html', {'professional': professional})
    except Professional.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not registered as a professional.'})


