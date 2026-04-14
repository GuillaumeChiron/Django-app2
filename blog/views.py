from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog import forms
from blog import models


@login_required
def home_page(request):
    photos = models.Photo.objects.all()
    return render(request, "blog/home_page.html", {"photos": photos})


@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == "POST":
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect("home-page")
    return render(request, "blog/photo_upload_page.html", context={"form": form})
