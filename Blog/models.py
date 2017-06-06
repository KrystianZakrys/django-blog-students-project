# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# class User(models.Model):
#     login = models.CharField(max_length=30)
#     haslo = models.CharField(max_length=24)
#     email = models.EmailField(max_length=254)
#
#     def __str__(self):
#         return self.login



class Tag(models.Model):
    nazwa = models.CharField(max_length=24)

    def __str__(self):
        return self.nazwa

    def __unicode__(self):
        return self.nazwa

class Post(models.Model):
    tytul = models.CharField(max_length=200)
    skrocona_tresc = models.CharField(max_length=350, blank=True)
    tresc = RichTextField()
    haslo = models.CharField(max_length=24, blank=True)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    obrazek_postu = models.FileField(null=True, blank=True)
    '''
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)'''

    def publish(self):
        self.data = timezone.now()
        self.save()

    def __str__(self):
        return self.tytul


class Obraz(models.Model):
    sciezka = models.FileField(max_length=100)




class PosTagi(models.Model):
    id_postu = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_tagu = models.ForeignKey(Tag, on_delete=models.CASCADE)


# class Komentarz(models.Model):
#     data = models.DateField(auto_now=False, auto_now_add=True)
#     id_usera = models.ForeignKey(User, on_delete=models.CASCADE)
#     tresc = models.TextField
#     id_postu = models.ForeignKey(Post,on_delete=models.CASCADE)
