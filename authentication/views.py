from django.shortcuts import render

# Create your views here.


def signup(request):
    print(dir(request))
    return render(request, 'signup.html')
