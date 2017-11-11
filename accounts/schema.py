import graphene
from graphene_django.types import DjangoObjectType
from hackathon.decorators import login_required

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query:
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    me = graphene.Field(UserType)

    @login_required
    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def resolve_me(self, info):
        return info.context.user
