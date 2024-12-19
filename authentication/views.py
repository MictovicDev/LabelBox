from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from annotation.models import Project



# Create your views here.
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        print(email, password, confirm_password)
        if password != confirm_password:
            messages.add_message(request, messages.INFO, 'PASSWORD DOES NOT MATCH')
            return render(request, 'signup.html')
        try:
            user = User.objects.create_user(email=email, password=password)
            user.is_active = True
            user.save()
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                response = HttpResponse()
                response['HX-Redirect'] = reverse('home') 
                return response
            else:
                messages.add_message(request, messages.INFO, 'Unable to log you in')
        except Exception as e:
            # Log error (instead of showing raw exception to the user)
            print(f"Error: {e}")
            messages.add_message(request, messages.INFO, f'An error occurred {e}. Please try again.')
            return render(request, 'signup.html')
        # User.objects.create(email=email, password=password)
    return render(request, 'signup.html')


def home(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user).filter(completed=False)[0:3]
        return render(request, 'annotate.html', context={'projects': projects})
    else:
        return redirect('signup.html')