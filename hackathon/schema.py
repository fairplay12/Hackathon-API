import graphene

from accounts.schema import Query as AccountsQuery
from accounts.mutations import (LoginMutation, RegisterMutation,
                                FacebookLoginMutation, GoogleLoginMutation)


class Query(AccountsQuery, RegisterMutation, FacebookLoginMutation,
            GoogleLoginMutation, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    facebook_login = FacebookLoginMutation.Field()
    google_login = GoogleLoginMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
