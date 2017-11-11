from django.db import models


class SportCategory(models.Model):
    name = models.CharField(
        max_length=255,
    )
    short_description = models.TextField()

    class Meta:
        verbose_name = 'Sport Category'
        verbose_name_plural = 'Sport Categories'

    def __str__(self):
        return str(self.name)


class SportSection(models.Model):
    category = models.ForeignKey(
        SportCategory,
        related_name='sport_sections',
    )
    name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    max_ppl_in_section = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.name)


class Achievement(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='achievements'
    )
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return str(self.user)


class Championship(models.Model):
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.name)


class CustomAchievement(models.Model):
    section = models.ForeignKey(
        SportSection,
        related_name='custom_achievements',
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.name)
