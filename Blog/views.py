# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Blog.forms import RegistrationForm, UserLoginForm, UserRegisterForm, PostAddForm
from .models import Post, Tag
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)


def logout_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    logout(request)
    authenticated = request.user.is_authenticated()
    print(request.user.is_authenticated())
    return redirect("/")


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated())
        return redirect("/")
    authenticated = request.user.is_authenticated()
    context = {
        'form': form,
        'title': title,
        'authenticated': authenticated}
    return render(request, "Blog/form.html", context)


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")
    context = {
        'form': form,
        'title': title,

    }
    return render(request, "Blog/form.html", context)


# def register(request):
#     authenticated = request.user.is_authenticated()
#     tagi =  tagi = Tag.objects.all()
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#
#         form = RegistrationForm()
#         args = {'form': form, 'tagi':tagi,'authenticated':authenticated}
#         return render(request, 'Blog/register.html', args)
#     else:
#         form = RegistrationForm()
#         args = {'form': form, 'tagi':tagi,'authenticated':authenticated}
#         return render(request, 'Blog/register.html', args)


# Create your views here.
def post_list(request):
    authenticated = request.user.is_authenticated()
    #print (authenticated)
    posty = Post.objects.all().order_by('-data')  # .filter(data=timezone.now()).order_by('data')
    query = request.GET.get("q")
    if query:
        posty = posty.filter(
            Q(tytul__icontains=query) |
            Q(skrocona_tresc__icontains=query) |
            Q(tresc__icontains=query) |
            Q(tags__nazwa__icontains=query)
        )
    query_tags = request.GET.get("qt")
    if query_tags:
        posty = posty.filter(tags__nazwa__icontains=query_tags)

    paginator = Paginator(posty, 7)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        posty = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posty = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posty = paginator.page(paginator.num_pages)

    tagi = Tag.objects.all()
    today = datetime.now()
    return render(request, 'Blog/post_list.html',
                  {'posty': posty, 'tagi': tagi, 'today': today, 'authenticated': authenticated})


def post_details(request, pk):
    authenticated = request.user.is_authenticated()
    post = Post.objects.get(pk=pk)
    tagi = Tag.objects.all()
    print(post.haslo)
    '''tutaj jeśli post ma hasło to zablokuj możliwość przekieruj na strone do wpisania hasła do postu --- AUTORYZACJA POSTU'''
    if not post.haslo is None and not post.haslo == '' : 
        if authenticated is False:
            return redirect(login_view)
        #return redirect(post_unlock(request,pk))
        return render(request, 'Blog/post_details.html',
                          {'post': post, 'tagi': tagi, 'authenticated': authenticated})
    else:
        return render(request, 'Blog/post_details.html', {'post': post, 'tagi': tagi, 'authenticated': authenticated})

@csrf_exempt
def add_post(request):
    wybor_tagow = Tag.objects.all()
    forma_PA = PostAddForm(request.POST, request.FILES)
    print(forma_PA)
    if request.is_ajax():
        print(forma_PA.errors)
        print(forma_PA.is_valid())
        print(forma_PA.cleaned_data)
        print(request.FILES['obrazek_postu'])
        if forma_PA.is_valid() :
            post = forma_PA.save(commit=False)
            current_user = request.user
            post.id_user_id = current_user.id
            print(request.POST.getlist('tagi'))

            for tag in request.POST.getlist('tagi'):
                tag = Tag.objects.get(pk=tag)
                print(tag)
                post.tags.add(tag)
            post.tresc = request.POST.get('html')
            post.save()
            forma_PA.save()
            # post.tresc = request.POST.get('html')
            # print(request.POST.getlist('tagi[]'))
            # post = Post(tytul=forma_PA.cleaned_data['tytul'],
            #             id_user_id=request.user.id,
            #             skrocona_tresc=forma_PA.cleaned_data['skrocona_tresc'],
            #             tresc=request.POST.get('html'),
            #             haslo=forma_PA.cleaned_data['haslo'],
            #             obrazek_postu=forma_PA.cleaned_data['obrazek_postu']
            #             )
            # post.save()
            # for tag in request.POST.getlist('tagi[]'):
            #     post.tags.add(tag)

    authenticated = request.user.is_authenticated()
    context = {
        'authenticated': authenticated,
        'form': forma_PA,
        'tagi': wybor_tagow,
    }
    return render(request, 'Blog/add_post.html', context)
