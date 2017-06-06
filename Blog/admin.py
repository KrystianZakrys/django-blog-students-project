# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Register your models here.
from django.contrib import admin
from .models import Post,  Tag
from django.contrib.auth.models import User


admin.site.register(Tag)
#admin.site.register(User)

class PostAdmin(admin.ModelAdmin):

    fields= ('tytul','skrocona_tresc','tresc','haslo','tags','obrazek_postu')

    def save_model(self, request, obj, form, change):
        obj.id_user = request.user
        obj.save()
#admin.site.register(Post)
admin.site.register(Post, PostAdmin)