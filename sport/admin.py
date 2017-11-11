from django.contrib import admin
from .models import (SportCategory, SportSection, Achievement,
                     Championship)

# Register your models here.
admin.site.register(SportCategory)
admin.site.register(SportSection)
admin.site.register(Achievement)
admin.site.register(Championship)
