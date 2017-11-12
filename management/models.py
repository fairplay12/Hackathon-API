from django.db import models


class Time(models.Model):
    sport_section = models.ForeignKey(
        'sport.SportSection',
        related_name='trainings_time',
    )
    time = models.DateTimeField()

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
