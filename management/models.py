from django.db import models


class Training(models.Model):
    DAYS = (
        (1, 'Пн'),
        (2, 'Вт'),
        (3, 'Ср'),
        (4, 'Чт'),
        (5, 'Пт'),
        (6, 'Сб'),
        (7, 'Вс'),
    )

    section = models.ForeignKey(
        'sport.SportSection',
        related_name='trainings'
    )
    day = models.PositiveSmallIntegerField(choices=DAYS)

    def __str__(self):
        return self.section.name


class Time(models.Model):
    training = models.ForeignKey(
        Training,
        related_name='training_times',
    )
    start_time = models.CharField(max_length=25)
    end_time = models.CharField(max_length=25)
    users = models.ManyToManyField('accounts.User')

    def __str__(self):
        return self.training.get_day_display()


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
