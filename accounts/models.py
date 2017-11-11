from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    sport_sections = models.ManyToManyField(
        'sport.SportSection',
        related_name='users',
        blank=True
    )
    custom_achievements = models.ManyToManyField(
        'sport.CustomAchievement',
        related_name='users',
        blank=True
    )
    expirience = models.PositiveSmallIntegerField(
        default=0
    )
    avatar = models.ImageField(
        upload_to='users/avatar/',
        null=True,
        blank=True,
    )
    about = models.TextField()
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    is_trainer = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.email


class SocialAssociation(models.Model):
    social_id = models.CharField(max_length=25)
    social_network = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name='social_association')

    def __str__(self):
        return self.user.email
