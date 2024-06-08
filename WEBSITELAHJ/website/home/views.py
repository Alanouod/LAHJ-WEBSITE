
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Homeowner, Professional, UserProfile,PreviousWork
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Professional
from django.contrib.auth import authenticate, login, logout
from .forms import HomeownerSignupForm, ProfessionalSignupForm
from .forms import HomeownerProfileForm, PhotoUploadForm
from .forms import HomeownerEditForm 
from .forms import PhotoUploadForm
from .forms import ProfessionalEditForm, PhotoUploadForm
from .forms import ProfessionalEditForm,ProfessionalSignupForm,PhotoUploadForm
from .models import PreviousWork, Wishlist,ProjectImage , Order
from .forms import ProjectPhotoUploadForm
from .models import ProjectImage
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ProjectPhotoUploadForm, ProjectDetailForm  
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse
from .forms import HomeownerPhotoUploadForm
from django.db.models import Avg
from .models import Professional, Rating
from django.db.models import Sum
from .forms import CommentForm, RatingForm
from .models import Professional, Comment, Rating
from django.db.models import Count
from decimal import Decimal
from .forms import OrderForm , MessageForm
from .models import Quote , Message
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'home.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def resource(request):
    return render(request, 'resource.html')

def findPro(request):
    return render(request, 'findPro.html')

def interior_designers(request):
    professionals = Professional.objects.filter(job='Interior-designer')
    return render(request, 'interior_designers.html' , {'professionals': professionals} )

def contractors(request):
    professionals = Professional.objects.filter(job='general-contractor')
    return render(request, 'contractors.html', {'professionals': professionals})

def kitchen_design(request):
    professionals = Professional.objects.filter(job='kitchen_designer')
    return render(request, 'kitchen_design.html' , {'professionals': professionals} )

def lighting_expert(request):
    professionals = Professional.objects.filter(job='lighting-expert')
    return render(request, 'lighting_expert.html' , {'professionals': professionals} )

def architects(request):
    professionals = Professional.objects.filter(job='architect')
    return render(request, 'architects.html' , {'professionals': professionals} )


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
            # Login the user
            user = authenticate(request, username=username, password=password)
            login(request, user)
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
                    password=form.cleaned_data['password'])
                professional = Professional.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    bio=form.cleaned_data['bio'],
                    job=form.cleaned_data['job'],
                    previous_work=request.FILES.get('previous_work'))        
                project = PreviousWork.objects.create(
                    professional=professional,
                    description="Description of the previous work",
                )
                ProjectImage.objects.create(project=project, image=professional.previous_work)
                user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
                login(request, user)
                return redirect('professional_profile', professional_id=professional.id)
    return render(request, 'joinAsPro.html', {'form': form, 'user_type': 'professional', 'messages': messages.get_messages(request)})

def user_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier') 
        password = request.POST.get('password')

        user = authenticate(request, email=identifier, password=password)

        if user is None:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            auth_login(request, user)  

            if getattr(user, 'homeowner', None):
                return redirect('homeowner_profile')
            elif getattr(user, 'professional', None):
                professional_id = user.professional.id
                return redirect(reverse('professional_profile', kwargs={'professional_id': professional_id}))

            else:
                error_message = 'حدث خطأ.'
                return render(request, 'user_login.html', {'error_message': error_message})
        else:
            error_message = "اسم المستخدم او كلمة المرور خاطئة"
            return render(request, 'user_login.html', {'error_message': error_message})
    else:
        return render(request, 'user_login.html')

def homeowner_profile(request):
    user = request.user
    homeowner = Homeowner.objects.get(user=user)
    sent_messages = Message.objects.filter(sender=homeowner.user)
    received_messages = Message.objects.filter(recipient=homeowner.user)
    wishlist_items = Wishlist.objects.filter(homeowner=homeowner)
    if request.method == 'POST':
        profile_form = HomeownerProfileForm(request.POST, instance=homeowner)
        if profile_form.is_valid():
            profile_form.save()

        photo_form = PhotoUploadForm(request.POST, request.FILES, instance=homeowner)
        if photo_form.is_valid():
            photo_form.save()

        return redirect('homeowner_profile')

    else:
        profile_form = HomeownerProfileForm(instance=homeowner)
        photo_form = PhotoUploadForm(instance=homeowner)
    orders = homeowner.orders.all()
    quotes = Quote.objects.filter(order__homeowner=homeowner)
    
    return render(request, 'homeowner_profile.html', {
        'homeowner': homeowner,
        'profile_form': profile_form,
        'photo_form': photo_form,
        'wishlist_items': wishlist_items,
        'orders': orders,
        'quotes': quotes, 
        'sent_messages': sent_messages,
        'received_messages': received_messages
})

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
    return redirect('homeowner_profile')


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
    if request.user.is_authenticated:
        homeowner = request.user.homeowner
        saved_photos = ProjectImage.objects.filter(project__wishlist__homeowner=homeowner)
        return render(request, 'wishlist_photos.html', {'saved_photos': saved_photos})
    else:
        return render(request, 'wishlist_photos.html')

def inspiration(request):
    previous_works = PreviousWork.objects.all()
    is_professional = False
    if request.user.is_authenticated and hasattr(request.user, 'professional'):
        is_professional = True
    return render(request, 'inspiration.html', {
        'previous_works': previous_works,
        'is_professional': is_professional
    })


@login_required
def save_photo_changes(request):
    if request.method == 'POST':
        photo_form = PhotoUploadForm(request.POST, request.FILES)

        if photo_form.is_valid():

            messages.success(request, 'Changes to the photo were saved successfully.')
        else:
            messages.error(request, 'Error saving changes to the photo. Please check the form.')

    return redirect('edit_photo') 


def professional_profile(request, professional_id):
    try:
        professional = Professional.objects.get(id=professional_id)
        comments = Comment.objects.filter(professional=professional)
        ratings = Rating.objects.filter(professional=professional)
        avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)
        num_ratings = ratings.count()

        orders = Order.objects.filter(professional=professional)
        messages = Message.objects.filter(recipient=professional.user).order_by('-date')
    except Professional.DoesNotExist:
        return render(request, 'error.html', {'message': 'Professional profile not found'})

    is_owner = False  
    if request.user.is_authenticated and hasattr(request.user, 'professional'):
        logged_in_professional = request.user.professional
        if logged_in_professional == professional:
            is_owner = True

    form = CommentForm()
    rating_form = RatingForm()
    message_form = MessageForm()

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
                # Save 
                rating = Rating.objects.create(
                    user=request.user,
                    professional=professional,
                    rating=rating_value,
                    comment=comment
                )
                rating.save()
                ratings = Rating.objects.filter(professional=professional)
                avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
                return redirect('professional_profile', professional_id=professional_id)

    return render(request, 'professional_profile.html', {
        'professional': professional,
        'is_owner': is_owner,
        'form': form,
        'rating_form': rating_form,
        'message_form': message_form,
        'comments': comments,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
        'orders': orders,
        'messages': messages,
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
            return redirect('professional_profile', professional_id=professional_id)
    else:
        return redirect('professional_profile', professional_id=professional_id)


@login_required
def submit_rating(request, professional_id):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        professional = Professional.objects.get(pk=professional_id)
        user = request.user
        if rating_value < 1 or rating_value > 5:
            messages.error(request, "Invalid rating value. Please select a rating between 1 and 5.")
            return redirect('professional_profile', professional_id=professional_id)
        existing_rating = Rating.objects.filter(user=user, professional=professional).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.comment = comment
            existing_rating.save()
        else:
            new_rating = Rating.objects.create(user=user, professional=professional, rating=rating_value, comment=comment)
            new_rating.save()
        avg_rating = Rating.objects.filter(professional=professional).aggregate(Avg('rating'))['rating__avg']
        professional.avg_rating = avg_rating
        professional.save()
        messages.success(request, "شكراً تم التقييم بنجاح")
        return redirect('professional_profile', professional_id=professional_id)
    else:
        return redirect('home')


@login_required
def edit_professional_profile(request):
    if not hasattr(request.user, 'professional'):
        raise Http404("ليس لديك الإذن للوصل لهذه الصفحة")
        
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
        raise Http404("ليس لديك الإذن للوصل لهذه الصفحة")
        
    professional = Professional.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=professional)
        if form.is_valid():
            form.save()
            return redirect('professional_profile', professional_id=professional.id)
    else:
        form = PhotoUploadForm(instance=professional)
    
    return render(request, 'professional_profile.html', {'form': form, 'professional': professional})


def user_profile(request):
    user = request.user

    try:
        homeowner = Homeowner.objects.get(user=user)
        return render(request, 'homeowner_profile.html', {'homeowner': homeowner})
    except Homeowner.DoesNotExist:
        try:
            professional = Professional.objects.get(user=user)
            return render(request, 'professional_profile.html', {'professional': professional})
        except Professional.DoesNotExist:
            return render(request, 'error.html', {'message': 'لست مسجل بالفعل ،قم بالتسجيل أولاً'})

def projects(request, professional_id=None):
    if professional_id:
        previous_works = PreviousWork.objects.filter(professional_id=professional_id)
        is_owner = request.user.is_authenticated and \
                   hasattr(request.user, 'professional') and \
                   request.user.professional.id == professional_id
    else:
        previous_works = PreviousWork.objects.all()
        is_owner = False  
    context = {
        'previous_works': previous_works,
        'is_owner': is_owner,
    }
    return render(request, 'projects.html', context)

@login_required
def add_project(request):
    if request.method == 'POST':
        detail_form = ProjectDetailForm(request.POST)
        photo_form = ProjectPhotoUploadForm(request.POST, request.FILES)
        if detail_form.is_valid() and photo_form.is_valid():
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
            return redirect('projects')  
    else:
        detail_form = ProjectDetailForm()
        photo_form = ProjectPhotoUploadForm()
    return render(request, 'add_project.html', {'detail_form': detail_form, 'photo_form': photo_form})


def project_details(request, project_id):
    project = get_object_or_404(PreviousWork, id=project_id)
    return render(request, 'project_details.html', {'project': project})

@login_required
def delete_project_image(request, image_id):
    if request.method == 'POST':
        project_image = get_object_or_404(ProjectImage, id=image_id)
        if project_image.project.professional.user == request.user:
            previous_work = project_image.project
            previous_work.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



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

def bohemian(request):
    return render(request, 'bohemian.html')

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
def submit_order(request, professional_id):
    professional = get_object_or_404(Professional, pk=professional_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            homeowner = request.user.homeowner
            order = form.save(commit=False)
            order.homeowner = homeowner
            order.professional = professional 
            order.status = 'في الانتظار'  
            order.save()
            return redirect('homeowner_profile')  
    else:
        form = OrderForm()
    
    return render(request, 'professional_profile.html', {'professional': professional, 'form': form})


@login_required
def view_orders(request):
    homeowner = request.user.homeowner
    orders = homeowner.orders.all()
    return render(request, 'homeowner_profile.html', {'homeowner': homeowner, 'orders': orders})

def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'مقبول'
    order.save()
    professional_id = order.professional.id
    return redirect('professional_profile', professional_id=professional_id)  

def decline_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'مرفوض'
    order.save()
    professional_id = order.professional.id
    return redirect('professional_profile', professional_id=professional_id)


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    professional_id = order.professional.id
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_details.html', {'order': order})

def submit_quote(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    professional = request.user.professional

    existing_quote = Quote.objects.filter(order=order, professional=professional).exists()

    if existing_quote:
        messages.error(request, "لقد قمت بالفعل بتقديم عرض لهذا الطلب")
    else:
        if request.method == 'POST':
            terms = request.POST.get('terms')
            cost = request.POST.get('cost')

            Quote.objects.create(
                professional=professional,
                order=order,
                terms=terms,
                cost=cost,
                status='في الانتظار'
            )
            messages.success(request, "تم تقديم عرضك بنجاح.")

    return redirect('professional_profile', professional_id=professional.id)

def get_quote_details(request, order_id):
    quotes = Quote.objects.filter(order__id=order_id)
    if quotes.exists():
        data = [{'id': quote.id, 'terms': quote.terms, 'cost': quote.cost, 'status': quote.status} for quote in quotes]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'No quotes found for this order.'}, status=404)

@require_http_methods(["POST"])
def accept_quote(request):
    quote_id = request.POST.get('quote_id')
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.status = 'مقبول'
    quote.save()
    return HttpResponse(status=204)

@require_http_methods(["POST"])
def decline_quote(request):
    quote_id = request.POST.get('quote_id')
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.status = 'مرفوض'
    quote.save()
    return HttpResponse(status=204)




@login_required
def start_message(request, professional_id):
    professional = get_object_or_404(Professional, pk=professional_id)
    recipient = professional.user

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['message_content']
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            messages.success(request, 'تم ارسال الرسالة بنجاح.. يمكنك الوصول للرسائل من ملفك الشخصي')
            return redirect('professional_profile', professional_id=professional_id)
        else:
            messages.error(request, 'حدث خطأ اثناء ارسال الرسالة... حاول مره أخرى')
    else:
        form = MessageForm()

    return render(request, 'professional_profile.html', {'professional': professional, 'form': form})

@login_required
def DM(request):
    user = request.user
    chat_threads = []  # List to store chat threads

    # Retrieve all messages involving the user
    sent_messages = Message.objects.filter(sender=user).order_by('-date')
    received_messages = Message.objects.filter(recipient=user).order_by('-date')

    # Group messages by recipient or sender
    chat_partners = set()
    for message in sent_messages:
        chat_partner = message.recipient
        if chat_partner not in chat_partners:
            chat_partners.add(chat_partner)
            chat_thread = {
                'partner': chat_partner,
                'last_message': message,
            }
            chat_threads.append(chat_thread)

    for message in received_messages:
        chat_partner = message.sender
        if chat_partner not in chat_partners:
            chat_partners.add(chat_partner)
            chat_thread = {
                'partner': chat_partner,
                'last_message': message,
            }
            chat_threads.append(chat_thread)

    return render(request, 'dm.html', {'chat_threads': chat_threads})

@login_required
def view_chat(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    partner = None
    if message.sender == request.user:
        partner = message.recipient
    elif message.recipient == request.user:
        partner = message.sender

    if partner is None:
        raise PermissionDenied

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=partner)) |
        (Q(sender=partner) & Q(recipient=request.user))
    ).order_by('date')

    return render(request, 'chat_detail.html', {'partner': partner, 'messages': messages})

@login_required
def reply_message(request, partner_id):
    partner = get_object_or_404(User, id=partner_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_content = form.cleaned_data['message_content']
            message = Message.objects.create(
                sender=request.user,
                recipient=partner,
                content=message_content
            )
            return redirect('view_chat', message_id=message.id)
    else:
        form = MessageForm()

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=partner)) |
        (Q(sender=partner) & Q(recipient=request.user))
    ).order_by('date')

    return render(request, 'chat_detail.html', {'partner': partner, 'messages': messages, 'form': form})


