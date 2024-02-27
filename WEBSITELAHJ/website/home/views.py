
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Homeowner, Professional
from .forms import HomeownerSignupForm, ProfessionalSignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import logout

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
                return render(request, 'signup.html', {'form': form, 'user_type': user_type, 'error_message': 'Username already exists. Please choose a different username.'})

            if user_type == 'homeowner':
                # Create Homeowner profile
                # You may add additional logic for homeowner profile creation
                pass
            elif user_type == 'professional':
                # Create Professional profile
                # You may add additional logic for professional profile creation
                pass

            # Log in the user
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('user_profile')

    else:
        user_type = request.GET.get('user_type')
        form = HomeownerSignupForm(initial={'user_type': user_type}) if user_type == 'homeowner' else ProfessionalSignupForm(initial={'user_type': user_type})

    return render(request, 'signup.html', {'form': form, 'user_type': user_type})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_profile')  # Redirect to user profile page
        else:
            error_message = 'Invalid email or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')



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





def services(request):
    return render(request, 'services.html')

def reso1(request):
    return render(request, 'reso1.html')

def refe(request):
    return render(request, 'refe.html')

def tips(request):
    return render(request, 'tips.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def user_profile(request):
    return render(request, 'user_profile.html')

def logout_view(request):
    logout(request)
    return render(request,'home.html')