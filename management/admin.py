from django.contrib import admin

from .models import Review, Time, Training

# Register your models here.
admin.site.register(Review)
admin.site.register(Time)
admin.site.register(Training)
