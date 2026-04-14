from django.contrib import admin
from blog.models import Photo, Blog


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("image", "caption", "uploader")


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Blog)
