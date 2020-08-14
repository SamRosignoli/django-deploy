from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):

  #creates a one to one relationship between UserProfileInfo and the default User model
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  #additional
  portfolio_site = models.URLField(blank=True) #black=True means it can be empty
  profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

  def __str__(self):
    return self.user.username