import graphene
from graphene_django.types import DjangoObjectType

from hackathon.decorators import login_required
from .models import User

from django.conf import settings


class UserType(DjangoObjectType):
    avatar = graphene.String()
    full_name = graphene.String()

    class Meta:
        model = User

    def resolve_avatar(self, info):
        return '{}{}'.format(settings.SITE_URL, self.avatar.url)

    def resolve_full_name(self, info):
        return self.get_full_name()


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
        if info.context.user.is_authenticated:
            return info.context.user
        else:
            return None
