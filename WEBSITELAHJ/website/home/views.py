
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Homeowner, Professional, UserProfile,PreviousWork
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
from .models import PreviousWork, Wishlist,ProjectImage
from .forms import ProjectPhotoUploadForm
from .models import ProjectImage
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ProjectPhotoUploadForm, ProjectDetailForm  
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Comment
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import HomeownerPhotoUploadForm
from django.db.models import Avg
from .models import Professional, Rating
from django.db.models import Sum
from .forms import CommentForm, RatingForm
from .models import Professional, Comment, Rating
from django.contrib import messages
from django.db.models import Count
from decimal import Decimal


def home(request):
    return render(request, 'home.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def resource(request):
    return render(request, 'resource.html')


@login_required
def save_to_wishlist(request, previous_work_id):
    previous_work = get_object_or_404(PreviousWork, id=previous_work_id)
    homeowner = request.user.homeowner

    # Check if the item is already in the wishlist
    if Wishlist.objects.filter(homeowner=homeowner, previous_work=previous_work).exists():
        # Item already exists in the wishlist, return JSON response with error message
        return JsonResponse({'success': False, 'message': 'العنصر موجود بالفعل في قائمة الأمنيات'})

    # Item is not in the wishlist, create a new Wishlist object
    Wishlist.objects.create(homeowner=homeowner, previous_work=previous_work)

    # Return JSON response with success message
    return JsonResponse({'success': True, 'message': 'تمت إضافة العنصر إلى قائمة الأمنيات بنجاح'})

def wishlist_photos(request):
    homeowner = request.user.homeowner
    saved_photos = Wishlist.objects.filter(homeowner=homeowner).values_list('previous_work__images__image', flat=True)
    return render(request, 'wishlist_photos.html', {'saved_photos': saved_photos})

def inspiration(request):
    previous_works = PreviousWork.objects.all()
    print(previous_works) 
    return render(request, 'inspiration.html', {'previous_works': previous_works})


def findPro(request):
    return render(request, 'findPro.html')



def signup(request):
    if request.method == 'POST':
        form = HomeownerSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'اسم المستخدم موجود بالفعل')
                return render(request, 'signup.html', {'form': form, 'user_type': 'homeowner'})
            if User.objects.filter(email=email).exists():
                messages.error(request, 'هذا البريد الإلكتروني مسجل بالفعل')
                return render(request, 'signup.html', {'form': form, 'user_type': 'homeowner'})
            
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
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'هذا البريد الإلكتروني مسجل بالفعل')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'اسم المستخدم موجود بالفعل')

            if not messages.get_messages(request):
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=form.cleaned_data['password']
                )
                professional = Professional.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    bio=form.cleaned_data['bio'],
                    job=form.cleaned_data['job'],
                    previous_work=request.FILES.get('previous_work') 
                )

                
                project = PreviousWork.objects.create(
                    professional=professional,
                    description="Description of the previous work",

                )

                # Associate the uploaded previous work with the new project
                ProjectImage.objects.create(project=project, image=professional.previous_work)

                user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
                login(request, user)

                return redirect('professional_profile', professional_id=professional.id)

    return render(request, 'joinAsPro.html', {'form': form, 'user_type': 'professional', 'messages': messages.get_messages(request)})

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
                # Check if the user is a professional and get their professional ID
                professional_id = user.professional.id
                # Redirect to the professional_profile with the professional ID included in the URL
                return redirect(reverse('professional_profile', kwargs={'professional_id': professional_id}))

            else:
                error_message = 'Invalid user type.'
                return render(request, 'user_login.html', {'error_message': error_message})
        else:
            error_message = 'Invalid email or password.'
            return render(request, 'user_login.html', {'error_message': error_message})
    else:
        return render(request, 'user_login.html')

def homeowner_profile(request):
    user = request.user
    homeowner = Homeowner.objects.get(user=user)
    wishlist_items = Wishlist.objects.filter(homeowner=homeowner)
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

    return render(request, 'homeowner_profile.html', {'homeowner': homeowner, 'profile_form': profile_form, 'photo_form': photo_form, 'wishlist_items': wishlist_items})


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
        photo_form = HomeownerPhotoUploadForm(request.POST, request.FILES, instance=homeowner)
        if photo_form.is_valid():
            photo_form.save()
            return redirect('homeowner_profile')

    else:
        photo_form = HomeownerPhotoUploadForm(instance=homeowner)

    return render(request, 'edit_photo.html', {'homeowner': homeowner, 'photo_form': photo_form})


@login_required
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

def professional_profile(request, professional_id):
    try:
        professional = Professional.objects.get(id=professional_id)
        comments = Comment.objects.filter(professional=professional)
        # Fetch all ratings associated with the professional
        ratings = Rating.objects.filter(professional=professional)
        # Calculate the average rating
        avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        # Round the average rating to two decimal places
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)
        # Calculate the number of ratings
        num_ratings = ratings.count()
    except Professional.DoesNotExist:
        return render(request, 'error.html', {'message': 'Professional profile not found'})

    is_owner = False  
    if request.user.is_authenticated and hasattr(request.user, 'professional'):
        logged_in_professional = request.user.professional
        if logged_in_professional == professional:
            is_owner = True

    if request.method == 'POST':
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.professional = professional
                comment.save()
                return redirect('professional_profile', professional_id=professional_id)
        elif 'rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating_value = rating_form.cleaned_data['rating']
                comment = rating_form.cleaned_data['comment']
                # Save the rating here
                rating = Rating.objects.create(
                    user=request.user,
                    professional=professional,
                    rating=rating_value,
                    comment=comment
                )
                rating.save()
                # Recalculate the average rating including the new rating
                ratings = Rating.objects.filter(professional=professional)
                avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
                # Redirect to the professional profile page after adding the rating
                return redirect('professional_profile', professional_id=professional_id)
    else:
        form = CommentForm()
        rating_form = RatingForm()

    return render(request, 'professional_profile.html', {
        'professional': professional,
        'is_owner': is_owner,
        'form': form,
        'rating_form': rating_form,
        'comments': comments,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
    })


@login_required
def add_comment(request, professional_id):
    professional = get_object_or_404(Professional, id=professional_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.professional = professional
            comment.save()
            # Redirect to the professional profile page after adding the comment
            return redirect('professional_profile', professional_id=professional_id)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form})

@login_required
def submit_rating(request, professional_id):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        professional = Professional.objects.get(pk=professional_id)
        user = request.user

        # Validate rating value
        if rating_value < 1 or rating_value > 5:
            messages.error(request, "Invalid rating value. Please select a rating between 1 and 5.")
            return redirect('professional_profile', professional_id=professional_id)

        # Handle non-AJAX request
        existing_rating = Rating.objects.filter(user=user, professional=professional).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.comment = comment
            existing_rating.save()
        else:
            new_rating = Rating.objects.create(user=user, professional=professional, rating=rating_value, comment=comment)
            new_rating.save()

        # Recalculate the average rating including all ratings
        avg_rating = Rating.objects.filter(professional=professional).aggregate(Avg('rating'))['rating__avg']
        professional.avg_rating = avg_rating
        professional.save()

        messages.success(request, "Rating submitted successfully.")
        return redirect('professional_profile', professional_id=professional_id)
    else:
        return redirect('home')


@login_required
def edit_professional_profile(request):
    if not hasattr(request.user, 'professional'):
        raise Http404("You do not have permission to access this page.")
        
    professional = Professional.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfessionalEditForm(request.POST, request.FILES, instance=professional)
        if form.is_valid():
            form.save()
            return redirect('professional_profile', professional_id=professional.id)
    else:
        form = ProfessionalEditForm(instance=professional)

    return render(request, 'edit_professional_profile.html', {'form': form, 'professional': professional})


@login_required
def edit_professional_photo(request):
    if not hasattr(request.user, 'professional'):
        raise Http404("You do not have permission to access this page.")
        
    professional = Professional.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=professional)
        if form.is_valid():
            form.save()
            return redirect('professional_profile', professional_id=professional.id)
    else:
        form = PhotoUploadForm(instance=professional)
    
    return render(request, 'edit_professional_photo.html', {'form': form, 'professional': professional})


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

def projects(request, professional_id=None):
    if professional_id:
        # Filter PreviousWork objects by the professional's ID
        previous_works = PreviousWork.objects.filter(professional_id=professional_id)
        # Check if the logged-in user is the owner of the professional profile
        is_owner = request.user.is_authenticated and \
                   hasattr(request.user, 'professional') and \
                   request.user.professional.id == professional_id
    else:
        # If no professional ID is provided, retrieve all PreviousWork objects
        previous_works = PreviousWork.objects.all()
        is_owner = False  # Since no professional_id is provided, there's no specific owner

    context = {
        'previous_works': previous_works,
        'is_owner': is_owner,
    }
    return render(request, 'projects.html', context)


@login_required
def delete_project_image(request, image_id):
    if request.method == 'POST':
        # Retrieve the project image object
        project_image = get_object_or_404(ProjectImage, id=image_id)
        # Check if the logged-in user is the owner of the image
        if project_image.project.professional.user == request.user:
            # Delete the associated PreviousWork object
            previous_work = project_image.project
            previous_work.delete()
            # Return success response
            return JsonResponse({'success': True})
    # Return failure response
    return JsonResponse({'success': False}, status=400)

@login_required
def add_project(request):
    if request.method == 'POST':
        # If the form is submitted, process the data
        detail_form = ProjectDetailForm(request.POST)
        photo_form = ProjectPhotoUploadForm(request.POST, request.FILES)

        if detail_form.is_valid() and photo_form.is_valid():
            # Save the project details
            project = detail_form.save(commit=False)
            project.professional = request.user.professional  
            project.save()

            # Save the project photo as a ProjectImage instance
            photo = photo_form.save(commit=False)
            photo.project = project
            photo.save()

            # If the professional has a registration photo, save it as a ProjectImage instance
            professional = request.user.professional
            if professional.previous_work:
                registration_photo = ProjectImage.objects.create(project=project, image=professional.previous_work)
                registration_photo.save()

            return redirect('projects')  # Redirect to the projects page after adding the project
    else:
        # If it's a GET request, just render the form
        detail_form = ProjectDetailForm()
        photo_form = ProjectPhotoUploadForm()

    return render(request, 'add_project.html', {'detail_form': detail_form, 'photo_form': photo_form})

def project_details(request, project_id):
    project = get_object_or_404(PreviousWork, id=project_id)
    return render(request, 'project_details.html', {'project': project})


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