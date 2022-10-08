from ast import Pass
from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def register_validator(self, posted_data):
        errors = {}
        for user in User.objects.all():
            if user.email == posted_data['email']:
                errors['duplicate_user'] = "Email already registered!"
                return errors
        if len(posted_data['first_name']) < 2:
            errors['first_name_lenth'] = "First name must be at least 2 characters!"

        if len(posted_data['last_name']) < 2:
            errors['last_name_lenth'] = "Last name must be at least 2 characters!"

        if str(posted_data['first_name']).isalpha() == False or str(posted_data['last_name']).isalpha() == False:
            errors['name_char'] = "Name must contain characters only!"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(posted_data['email']):          
            errors['email'] = "Invalid email address!"
    
        if len(posted_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters length!"

        if posted_data['confirm_password'] != posted_data['password']:
            errors['password_match'] = "Password didn't match!"

        if posted_data['birth_date'] > str(datetime.now()):
            errors['birth_date'] = "Birth date must be in the past!"
        
        date_now = date.today()
        birth_date = datetime.strptime(posted_data['birth_date'], "%Y-%m-%d")
        age = date_now.year - birth_date.year - ((date_now.month, date_now.day) < (birth_date.month, birth_date.day))
        
        if age < 13:
            errors['birth_date2'] = "You must to be older than 13 years old to be able to register!"
    

        return errors

    def login_validator(self, posted_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(posted_data['email']):          
            errors['email'] = "Invalid email address!"
            return errors
        
        if not User.objects.filter(email = posted_data['email']):
            errors['unregistered_user'] = "Email not registered!"
                
        return errors
  
        
        


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    birth_date =  models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()