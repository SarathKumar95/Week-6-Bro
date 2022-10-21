from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context

from owner.forms import CustomUserCreationForm
from owner.models import CustomUser


# Create your views here.


def signup(request):
    if 'customer' in request.session:
        return redirect('home')

    form = CustomUserCreationForm
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            print('form saved')
            form.save()
            messages.info(request, "User created.You can log in here.")
            return redirect('signin')

        else:
            print(form.errors)

    return render(request, 'owner/signup.html', context)


def signin(request):
    if 'customer' in request.session:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['customer'] = username
            print('Hey this user is : ' + request.session['customer'])
            return redirect(home)

        elif user is None:
            messages.info(request, "User does not exist. Check credentials")

    return render(request, 'owner/signin.html')


def home(request):
    if 'customer' in request.session:
        temp = {"username": request.session['customer']}
        context = {'temp': temp}
        return render(request, 'owner/home.html', context)

    return redirect('signin')


def out(request):
    if 'customer' in request.session:
        del request.session['customer']
    messages.success(request, "Thank you for spending time with us.")
    return redirect('signin')


def owner(request):
    user = CustomUser.objects.all()
    context = {'user': user}
    return render(request, 'owner/dashboard.html', context)

    # return redirect('/')


def create_user(request):
    form = CustomUserCreationForm
    context = {'form': form}

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "The user has been created.")
            return redirect('owner')

        else:
            print(form.errors)

    return render(request, 'owner/create.html', context)


def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect('owner')


def master(request):
    if 'superuser' in request.session:
        return redirect('owner')

    if request.method == "POST":
        admin = request.POST['uname']
        pword = request.POST['pwd']

        user = authenticate(username=admin, password=pword)

        if user is not None and user.is_superuser:
            request.session['superuser'] = admin
            print(request.session['superuser'])
            return redirect('owner')

        else:
            messages.info(request, "You don't seem to be an admin.Check credentials")

    return render(request, 'owner/master.html')


def masterout(request):
    if 'superuser' in request.session:
        del request.session['superuser']
        return redirect(master)