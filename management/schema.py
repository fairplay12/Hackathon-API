import graphene
from graphene_django.types import DjangoObjectType

from .models import Review, Time, Training


class ReviewType(DjangoObjectType):

    class Meta:
        model = Review


class TimeType(DjangoObjectType):
    class Meta:
        model = Time


class TrainingType(DjangoObjectType):
    day_display = graphene.String()

    class Meta:
        model = Training

    def resolve_day_display(self, info):
        return self.get_day_display()


class Query:
    reviews_about_section = graphene.List(
        ReviewType,
        section_id=graphene.ID()
    )
    reviews_by_user = graphene.List(
        ReviewType,
        user_id=graphene.ID()
    )

    def resolve_reviews_about_section(self, info, section_id):
        return Review.objects.filter(section_id=section_id)

    def resolve_reviews_by_user(self, info, user_id):
        return Review.objects.filter(user_id=user_id)
