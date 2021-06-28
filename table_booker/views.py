from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def home_page(request):
    return render(request, "home.html", context={})


def login_page(request):
    return render(request, "login.html", context={})


def signup_page(request):
    return render(request, "signup.html", context={})


def logout_page(request):
    return render(request, "logout.html", context={})

# Create your views here.
