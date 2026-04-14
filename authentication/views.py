from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from . import forms

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    pass


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup_page.html", {"form": form})


@login_required
def upload_profil_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == "POST":
        form = forms.UploadProfilePhotoForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("home-page")
    return render(request, "authentication/upload_profil_photo.html", {"form": form})
