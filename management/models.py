from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Schedule(models.Model):
    sport_section = models.OneToOneField(
        'sport.SportSection',
        related_name='schedule',
    )
    time = ArrayField(JSONField())

    def __str__(self):
        return self.sport_section
