import graphene
from graphene_django.types import DjangoObjectType
from hackathon.decorators import login_required

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query:
    users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        return User.objects.all()
