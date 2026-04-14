from django import forms
from blog import models


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ["image", "caption"]
