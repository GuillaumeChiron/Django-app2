from django import forms
from blog import models


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ["image", "caption"]


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title", "content"]
