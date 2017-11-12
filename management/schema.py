import graphene
from graphene_django.types import DjangoObjectType

from .models import Review, Time


class ReviewType(DjangoObjectType):

    class Meta:
        model = Review


class TimeType(DjangoObjectType):

    class Meta:
        model = Time


class Query:
    reviews_about_section = graphene.List(
        ReviewType,
        section_id=graphene.ID()
    )
    reviews_by_user = graphene.List(
        ReviewType,
        user_id=graphene.ID()
    )
    trainings_time = graphene.List(
        TimeType,
        section_id=graphene.ID()
    )

    def resolve_reviews_about_section(self, info, section_id):
        return Review.objects.filter(section_id=section_id)

    def resolve_reviews_by_user(self, info, user_id):
        return Review.objects.filter(user_id=user_id)

    def resolve_trainings_time(self, info, section_id):
        return Time.objects.filter(sport_section_id=section_id)
