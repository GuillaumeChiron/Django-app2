from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = ""

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                message = f"identifiants incorrects"

    return render(request, "authentication/login_page.html", {"form": form, "message": message})


def logout_user(request):
    logout(request)
    return redirect("login-page")