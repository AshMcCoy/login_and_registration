from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name']= " First Name must be more than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name']= "Last Name must be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):  
            errors['email']= "Invalid email address!"
        userEmail = User.objects.filter(email = postData['email'])
        if len(userEmail) >= 1:
            errors['duplicate'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password']= " Password must be more than 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['pw_match']= "Password must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length= 75)
    email = models.CharField(max_length= 75)
    password = models.CharField(max_length= 75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
