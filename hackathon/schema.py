import graphene

from accounts.schema import Query as AccountsQuery
from accounts.mutations import (LoginMutation, RegisterMutation,
                                FacebookLoginMutation, GoogleLoginMutation)
from sport.schema import Query as SportQuery
from sport.mutations import (CreateSportCategoryMutation,
                             CreateSportSectionMutation)


class Query(AccountsQuery, RegisterMutation, FacebookLoginMutation,
            GoogleLoginMutation,
            SportQuery, CreateSportCategoryMutation,
            CreateSportSectionMutation, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    facebook_login = FacebookLoginMutation.Field()
    google_login = GoogleLoginMutation.Field()
    create_sport_category = CreateSportCategoryMutation.Field()
    create_sport_section = CreateSportSectionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
