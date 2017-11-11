import graphene
from graphene_django.types import DjangoObjectType
from hackathon.decorators import login_required

from .models import SportCategory, SportSection, Achievement, Championship


class SportCategoryType(DjangoObjectType):
    class Meta:
        model = SportCategory


class SportSectionType(DjangoObjectType):
    class Meta:
        model = SportSection


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement


class ChampionshipType(DjangoObjectType):
    class Meta:
        model = Championship


class Query:
    sport_categories = graphene.List(SportCategoryType)
    sport_sections = graphene.List(SportSectionType, id=graphene.ID())

    def resolve_sport_categories(self, info):
        return SportCategory.objects.all()

    def resolve_sport_sections(self, info, id):
        return SportSection.objects.filter(category_id=id)
