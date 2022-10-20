from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from owner.forms import CustomUserCreationForm


# Create your views here.


def signup(request):
    form = CustomUserCreationForm
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            print('form saved')
            form.save()

        else:
            print(form.errors)

    return render(request, 'owner/signup.html', context)


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            return redirect('home')

        elif user is None:
            messages.info(request, "User does not exist. Check credentials")

    return render(request, 'owner/signin.html')


def home(request):
    return render(request, 'owner/home.html')


def out(request):
    logout(request)
    return redirect('signin')
