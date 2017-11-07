from django.contrib import admin

from .models import User, SocialAssociation
# Register your models here.

admin.site.register(User)
admin.site.register(SocialAssociation)
