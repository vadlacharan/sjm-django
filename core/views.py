from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout, get_user_model
from .models import Publication, Comment, Likes, Saved, News


# Create your views here.


def homepage(request):
    return render(request, "home.html")


def aboutpage(request):
    return HttpResponse("Hello World")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        user = authenticate(request, username=email, password=password)
        print(user)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("publications")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "signin.html")
def signup_page(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = f"{firstname} {lastname}"  # Allow duplicate usernames
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validations
        if not firstname or not lastname or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        else:
            try:
                validate_email(email) 
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                login(request,user)
                messages.success(request, "Account created successfully!")
                return redirect("homepage")  

            except ValidationError:
                messages.error(request, "Invalid email format.")
            except IntegrityError:
                messages.error(request, "Email already registered.")  

    return render(request, "signup.html")



def publication_detail(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    
    # Get the user ID if authenticated
    user_id = request.user.id if request.user.is_authenticated else None

    # Check if the user has liked or saved the publication
    liked = Likes.objects.filter(user_id=user_id, publication_id=publication.id).exists() if user_id else False
    saved = Saved.objects.filter(user_id=user_id, publication_id=publication.id).exists() if user_id else False
    
    # Count total likes
    like_count = Likes.objects.filter(publication_id=publication.id).count()
    
    # Get all comments
    comments = Comment.objects.filter(publication_id=publication.id).order_by("-created_at")

    # Handle new comment submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to comment.")
            return redirect("login_page")

        comment_value = request.POST.get("comment_value", "").strip()  # Ensure input isn't just whitespace

        if comment_value:
            Comment.objects.create(
                user_id=request.user.id,  # Save user ID directly
                publication_id=publication.id,
                comment_value=comment_value,
            )
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Comment cannot be empty.")

        return redirect("publication_detail", slug=publication.slug)  # Avoid duplicate form resubmission

    context = {
        "publication": publication,
        "comments": comments,
        "liked": liked,
        "saved": saved,
        "like_count": like_count,
    }

    return render(request, "publication.html", context)

@login_required
def like_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user_id = request.user.id  

    if Likes.objects.filter(user_id=user_id, publication_id=publication.id).exists():
        Likes.objects.filter(user_id=user_id, publication_id=publication.id).delete()
        messages.success(request, "You unliked this publication.")
    else:
        Likes.objects.create(user_id=user_id, publication_id=publication.id)
        messages.success(request, "You liked this publication.")

    return redirect("publication_detail", slug=publication.slug)




def publications_page(request):
    #fetch all publications from publication model only title and likes
    publications = Publication.objects.all().values('title', 'likes', 'slug')
    publications_list = list(publications)
    print(publications_list)
    #pass publication as context
    context = {'publications': publications_list}
    return  render(request, "publications.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("homepage")


@login_required
def like_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user_id = request.user.id  # Get the logged-in user’s ID

    # Check if the user already liked the publication
    like_exists = Likes.objects.filter(user_id=user_id, publication_id=publication.id).exists()

    if like_exists:
        Likes.objects.filter(user_id=user_id, publication_id=publication.id).delete()
        messages.success(request, "You unliked this publication.")
    else:
        Likes.objects.create(user_id=user_id, publication_id=publication.id)
        messages.success(request, "You liked this publication.")

    return redirect("publication_detail", slug=publication.slug)


@login_required
def save_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user_id = request.user.id  

    # Check if the user already saved the publication
    save_exists = Saved.objects.filter(user_id=user_id, publication_id=publication.id).exists()

    if save_exists:
        Saved.objects.filter(user_id=user_id, publication_id=publication.id).delete()
        messages.success(request, "You removed this publication from saved.")
    else:
        Saved.objects.create(user_id=user_id, publication_id=publication.id)
        messages.success(request, "You saved this publication.")

    return redirect("publication_detail", slug=publication.slug)


def announcements_view(request):
    announcements = News.objects.all().order_by('-created_at')

    return render(request, 'announcements.html', {'announcements': announcements})