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


class Review(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='reviews'
    )
    section = models.ForeignKey(
        'sport.SportSection',
        related_name='reviews'
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.user.get_full_name()
