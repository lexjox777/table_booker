from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import UserForm, BookingForm
from .models import Restaurant

def home_page(request):
    if not request.user.is_authenticated:
        return redirect("table_booker:login")

    context = {"restaurants": Restaurant.objects.all()}
    return render(request, "home.html", context=context)

def book_restaurant(request, restaurant_id):
   if not request.user.is_authenticated:
        return redirect("table_booker:login")

   try:
      restaurant = Restaurant.objects.get(id=restaurant_id)
   except Restaurant.DoesNotExist:
      restaurant = None

   if restaurant is None:
      message.error(request, "Invalid restaurant supplied")
      return redirect("table_booker:home")

   if request.method=="POST":
      form = BookingForm(request.POST)

      if form.is_valid():
        booking=form.save(commit=False)
        booking.restaurant=restaurant
        booking.user=request.user
        booking.save()
        messages.info(request,f"You successfully booked{restaurant}")
        return redirect("table_booker:home")
   else:
      form= BookingForm

   return render(request=request, template_name="book_restaurant.html", context={"booking_form": form},)



def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("table_booker:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="login.html",
        context={"login_form": form},
    )


def signup_page(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("table_booker:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    return render(
        request=request,
        template_name="signup.html",
        context={"register_form": form},
    )


def logout_page(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("table_booker:login")

