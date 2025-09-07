from django.shortcuts import render
from django.http import JsonResponse 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , get_object_or_404 ,redirect
from django.urls import reverse
from django.utils import timezone
from .models import User 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume
from .crewai_pipeline.runner import run_nexus_crew


def index(request):
    success = False
    message = None  

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_obj = form.save()

            # Run CrewAI pipeline on the uploaded file
            resume_path = resume_obj.file.path
            candidate_email = request.POST.get("email")  # <-- get email from form

            try:
                run_nexus_crew(resume_path, candidate_email)  # pipeline now sends email
                success = True
                message = "✅ Resume submitted successfully. We’ll notify you by email."
            except Exception as e:
                message = f"❌ Error while processing resume: {e}"

            # Reset the form after saving
            form = ResumeForm()
    else:
        form = ResumeForm()

    return render(request, 'app/index.html', {
        'form': form,
        'success': success,
        'message': message,
    })

def success(request):
    return render(request, 'app/success.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")