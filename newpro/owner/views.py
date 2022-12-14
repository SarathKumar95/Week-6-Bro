from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.views.decorators.cache import cache_control

from owner.forms import CustomUserCreationForm, CustomUserChangeForm
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
            messages.info(request,form.errors)
    return render(request, 'owner/signup.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True,no_store=True)
def owner(request):
    if 'superuser' in request.session:
        user = CustomUser.objects.all()
        context = {'user': user}
        return render(request, 'owner/dashboard.html', context)

    return redirect('master')

@cache_control(no_cache = True, must_revaliate=True, no_store=True)
def create_user(request):
    if 'superuser' not in request.session:
        return redirect('master')

    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "The user has been created.")
            return redirect('owner')

        else:
            print(form.errors)
            messages.error(request, form.errors)

    return render(request, 'owner/create.html', context)


@cache_control(no_cache=True,no_store=True)
def delete_user(request, id):

    if 'superuser' in request.session:
        user = CustomUser.objects.get(id=id)
        user.delete()
        messages.success(request,str(user) + " is deleted.")
        return redirect('owner')

    return redirect('master')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


def search_user(request):
    if request.method == "POST":
        searched = request.POST['searched']
        user = CustomUser.objects.filter(username__contains=searched)
        return render(request, 'owner/dashboard.html', {'searched': searched, 'user': user})

    else:
        return redirect(owner)

@cache_control(no_cache=True,no_store=True)
def update_user(request, id):
    if 'superuser' in request.session:
        user = CustomUser.objects.get(id=id)
        form = CustomUserChangeForm(instance=user)

        old_username = user
        old_email = user.email

        if request.method == 'POST':


            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                print("Old username in post is ", old_username)
                print("Old email in post is ", old_email)
                new_username = request.POST['username']
                new_email = request.POST['email']
                print("new username is ",new_username,"and new email is",new_email)

                form.save()
                print("Updated")

                messages.info(request,'User with user id ' + str(user.id) + " has been updated. ")

                return redirect('owner')

            else:
                print("Edit unsuccesful" + str(form.errors))
                messages.error(request, form.errors)

        return render(request, 'owner/edit.html', {'form': form})

    else:
        return redirect('master')