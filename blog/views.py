from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from blog import forms
from blog import models


@login_required
def home_page(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()
    return render(request, "blog/home_page.html", {"photos": photos, "blogs": blogs})


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


@login_required
def blog_and_photo_upload(request):
    photo_form = forms.PhotoForm()
    blog_form = forms.BlogForm()
    if request.method == "POST":
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        blog_form = forms.BlogForm(request.POST)
        if all([photo_form.is_valid(), blog_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect("home-page")
    return render(
        request,
        "blog/create_blog_post.html",
        {"photo_form": photo_form, "blog_form": blog_form},
    )


@login_required
def blog_view(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, "blog/view_blog.html", {"blog": blog})


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == "POST":
        if "edit_form" in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("home-page")
        if "delete_form" in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            blog.delete()
            return redirect("home-page")
    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
        "blog": blog,
    }
    return render(request, "blog/edit_blog.html", context=context)


@login_required
def create_multiple_photos(request):
    PhotoFormset = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormset()
    if request.method == "POST":
        formset = PhotoFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
                    return redirect("home-page")
    return render(request, "blog/create_multiple_photos.html", {"formset": formset})
