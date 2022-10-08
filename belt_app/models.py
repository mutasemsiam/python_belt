from django.db import models
from login_app.models import User

class TreeManager(models.Manager):
    
    def tree_validator(self, posted_data):
        errors = {}
        if len(posted_data['species']) < 5:
            errors['species'] = "Species must be at least 5 characters length!"
        if len(posted_data['location']) < 2:
            errors['location'] = "Location must be at least 2 characters length!"
        if len(posted_data['reason']) > 50:
            errors['reason'] = "Reason must be at most 50 characters length!"
                
        return errors

class Tree(models.Model):
    species = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="trees", on_delete = models.CASCADE)
    location = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    date_planted = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TreeManager()


    
