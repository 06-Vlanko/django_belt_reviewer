# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.messages import get_messages

from .models import *

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect ('/books')
    return render (request, 'books_reviews/index.html')

def dashboard(request):
    print '----> REQUEST.SESSION.ALIAS:', request.session['alias']
    return render (request, 'books_reviews/dashboard.html')

def logout(request):
    request.session.clear()
    return redirect ('/')

def add(request):
    return render (request, 'books_reviews/add_book.html')

def register(request):
    #if there are errors in the validator, it will return a dic with a single key
    #otherwise, it will return the id of the newly created user
    result = User.objects.regValidator(request.POST)

    if 'registration' in result:
        for tag,_list in result.iteritems():
            for error in _list:
                messages.error(request, error, extra_tags=tag)
        return redirect ('/')
    else:
        print '-----> ATTEMPTING TO LOAD USER ID/NAME INTO SESSION (A)'
        request.session ['user_id']=result['user'].id
        request.session ['alias']=User.objects.get(id=result['user'].id).alias
        print '-----> ATTEMPTING TO LOAD USER ID/NAME INTO SESSION (A)'
        return redirect ('/books')


def login(request):
    #this will either return a disctionary that holds the errors messages
    #or the id of the logged in user if there were no errors on the form validation
    result = User.objects.logValidator(request.POST)

    if 'login' in result:
        for tag,_list in result.iteritems():
            for error in _list:
                messages.error(request, error, extra_tags=tag)
        return redirect ('/')
    else:
        request.session ['user_id']=result['user'].id
        request.session ['alias']=User.objects.get(id=result['user'].id).alias
        return redirect ('/books')

def create_book (request):
    result = Review.objects.reviewValidator(request.POST)
    pass