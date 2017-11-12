import graphene
from accounts.schema import UserType
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from graphene_django.converter import convert_django_field
from graphene_django.types import DjangoObjectType

from .models import (Achievement, Championship, CustomAchievement,
                     SportCategory, SportSection)
from .scalars import LocationScalar

# from hackathon.decorators import login_required


@convert_django_field.register(JSONField)
def convert_location_field(field, registry=None):
    return LocationScalar()


class SportCategoryType(DjangoObjectType):
    image = graphene.String()

    class Meta:
        model = SportCategory

    def resolve_image(self, info):
        return '{}{}'.format(settings.SITE_URL, self.image.url)


class SportSectionType(DjangoObjectType):
    trainers = graphene.List(UserType)
    image = graphene.String()

    def resolve_trainers(self, info):
        return self.users.filter(is_trainer=True)

    def resolve_image(self, info):
        return '{}{}'.format(settings.SITE_URL, self.image.url)

    class Meta:
        model = SportSection


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement


class ChampionshipType(DjangoObjectType):
    class Meta:
        model = Championship


class CustomAchievementType(DjangoObjectType):
    class Meta:
        model = CustomAchievement


class Query:
    sport_categories = graphene.List(SportCategoryType)
    sport_sections = graphene.List(SportSectionType, category_id=graphene.ID())
    sport_section = graphene.Field(SportSectionType, id=graphene.ID())

    def resolve_sport_categories(self, info):
        return SportCategory.objects.all()

    def resolve_sport_sections(self, info, category_id):
        return SportSection.objects.filter(category_id=category_id)

    def resolve_sport_section(self, info, id):
        try:
            return SportSection.objects.get(pk=id)
        except SportSection.DoesNotExist:
            return None
