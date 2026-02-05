# from django.db import models

# # Create your models here.
##This is Serializer (practicing here)

from django.db import models
class ChatBotModel(models.Model):
    prompt=models.TextField(max_length=40)
    ai=models.TextField(max_length=40)
    
    def __str__(self):
        return self.ai 
    
from django.contrib.auth.models import User    
class ProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')    
    profile_pic=models.ImageField(upload_to='profile_pic',null=True,blank=True)
    
    def __str__(self):
        return self.user.username