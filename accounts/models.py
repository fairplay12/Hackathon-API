from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.email


class SocialAssociation(models.Model):
    social_id = models.CharField(max_length=25)
    social_network = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name='social_association')

    def __str__(self):
        return self.user.email
