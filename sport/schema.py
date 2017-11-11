import graphene
from accounts.schema import UserType
from graphene_django.types import DjangoObjectType

from .models import (Achievement, Championship, CustomAchievement,
                     SportCategory, SportSection)

# from hackathon.decorators import login_required



class SportCategoryType(DjangoObjectType):
    class Meta:
        model = SportCategory


class SportSectionType(DjangoObjectType):
    trainers = graphene.List(UserType)

    def resolve_trainers(self, info):
        return self.users.filter(is_trainer=True)

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

    def resolve_sport_categories(self, info):
        return SportCategory.objects.all()

    def resolve_sport_sections(self, info, category_id):
        return SportSection.objects.filter(category_id=category_id)
