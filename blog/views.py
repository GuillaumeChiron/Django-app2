from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms import formset_factory

from itertools import chain

from blog import forms
from blog import models


@login_required
def home_page(request):
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) | Q(starred=True)
    )

    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()
    ).exclude(blog__in=blogs)
    blogs_and_photos = sorted(
        chain(blogs, photos), key=lambda x: x.date_created, reverse=True
    )

    paginator = Paginator(blogs_and_photos, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/home_page.html", {"page_obj": page_obj})


@login_required
@permission_required("blog.add_photo", raise_exception=True)
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
@permission_required("blog.add_blog", raise_exception=True)
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
            blog.photo = photo
            blog.save()
            blog.contributors.add(
                request.user, through_defaults={"contribution": "Auteur principal"}
            )
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
@permission_required("blog.add_blog", raise_exception=True)
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
@permission_required("blog.add_photo", raise_exception=True)
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


@login_required
def follow_usrers(request):
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home-page")
    return render(request, "blog/follow_users_form.html", {"form": form})
