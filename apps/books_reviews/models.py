# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
# Create your models here.

class UserManager (models.Manager):
    def regValidator (self, postData):
        errors = {
            'registration': []
        }

        #verfies the length of string entered in the first_name field is >= 2
        if len(postData['name'])<2:
            errors['registration'].append ('The "Name" should be at least 2 characters')
        else: #verifies if all characters in first_name are letters
            for character in postData['name']:
                if not NAME_REGEX.match(postData['name']):
                    errors['registration'].append('The "Name" field should only contain letters')
                    break

        #verifies the email value
        if len(postData['email'])<1:
            errors['registration'].append ('The "Email" field cannot be empty')
        #checks if the email is in the format something@something.some
        elif not EMAIL_REGEX.match(postData['email']):
            errors['registration'].append ("The email address you entered is invalid")
        else: #checks if the email is already in use by an existing user
            try:
                User.objects.get(email = postData['email'])
                errors['registration'].append ('The email address you entered is already in use, please use a different email address')
            except:
                #do nothing
                print '----> THE EMAIL IS AVAILABLE'

        #verifies the password
        if len(postData['password'])<1:
            errors['registration'].append ('The "Password" field cannot be empty')
        #checks the length of the value entered in the password field, if its less than 8 redirects
        elif len(postData['password'])<=8:
            errors['registration'].append ('The password must be more than 8 characters')
        #checks the confirm_password value
        if len(postData['confirm_password'])<1:
            errors['registration'].append ('The "Confirm Password" field cannot be empty')
        #checks that the password and confirm password lengths match
        if len(postData['password']) != len(postData['confirm_password']):
            errors['registration'].append ('The password and confirm password values should match')
        else: #if the lengths match, check if characters are an exact match
            for index in range ( len(postData['password']) ):
                if postData['password'][index] != postData['confirm_password'][index]:
                    errors['registration'].append ('The password and confirm password values must match')
                    break
        
        if len(errors['registration'])>0:
            return errors
        else:
            encrypted_pass = bcrypt.hashpw ( postData['password'].encode(), bcrypt.gensalt() )
            user = self.create(
                name = postData['name'],
                alias = postData['alias'],
                email = postData['email'],
                password = encrypted_pass
            )
            return { 'user': user }

    def logValidator (self, postData):
        errors = {
            'login': []
        }

        #verifies the email is n ot empty
        if len(postData['email'])<1:
            errors['login'].append ('The "Email" field cannot be empty')
        #checks if the email is in the format something@something.some
        elif not EMAIL_REGEX.match(postData['email']):
            errors['login'].append ("Invalid email address")
        #verifies the password is not empty
        if len(postData['password'])<1:
            errors['login'].append ('The "Password" field cannot be empty')

        if len(errors['login'])>0:
            return errors
        else:
            try:#tries to get the user from the db
                user = User.objects.get(email=postData['email'])
            except:
                print '-----> COULD NOT FIND THE USER'
                errors['login'].append ('The email and password combination that you entered does not match our records, please try again')
                return errors
            print '-----> FOUND USER: ', user
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print '-----> THE PASSWORDS MATCH!'
                return { 'user': user }
            else:
                errors['login'].append ('The email and password combination that you entered does not match our records, please try again')
                print '-----> THE PASSWORDS DO NOT MATCH!'
                return  errors

class User (models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return self.name

class Author (models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Book (models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey (Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class ReviewManager (models.Manager):
    def reviewValidator(self, postData):
        result = []
        if len(postData['title'])<1:
            result.append ('Please enter a title')
        
        return result

class Review (models.Model):
    content =  models.TextField()
    rating = models.IntegerField()
    creator = models.ForeignKey(User, related_name='user_reviews')
    book = models.ForeignKey(Book, related_name='book_reviews')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = ReviewManager()

    def __str__(self):
        return self.rating