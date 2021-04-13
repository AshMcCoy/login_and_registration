from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'index.html')

def createUser(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)

        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        newUser = User.objects.create(
            first_name= request.POST['first_name'],
            last_name= request.POST['last_name'],
            email= request.POST['email'],
            password= hash_pw
        )
        request.session['logged_in_user'] = newUser.id
        messages.success(request, "You have successfully registered!")
        return redirect('/user/success')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_in_user'] = log_user.id
                messages.success(request, "You have successfully logged in!")
                return redirect('/user/success')
            messages.error(request, "Email or password are invalid")

    return redirect('/')


def success(request):    
    context = {
        'logged_in_user' : User.objects.get(id=request.session['logged_in_user'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    print("user logged out")
    return redirect('/')