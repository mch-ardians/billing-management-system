from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib import messages

# Create your views here.
def sign_in(request) :
    form = LoginForm()
    
    if request.method == "POST" :    
        user = None
        
        username = request.POST["username"]
        password = request.POST["password"]
            
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard:index"))
        else:
            messages.error(request, "Invalid username or password")
            
    # errors = form.errors
            
    context = {
        'title' : "Login",
        'form_username' : form['username'],
        'form_password' : form['password'],
        # "errors" : errors, 
    }
    
    return render(request, "login.html", context)

def sign_out(request) :
    if request.method == "POST" and request.POST["logout"] == "Submit":
        logout(request)
            
        return HttpResponseRedirect(reverse("authenticate:login"))