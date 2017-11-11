import graphene

from accounts.schema import Query as AccountsQuery
from accounts.mutations import (LoginMutation, RegisterMutation,
                                FacebookLoginMutation, GoogleLoginMutation,
                                UpdateUserMutation)
from sport.schema import Query as SportQuery
from sport.mutations import (CreateSportCategoryMutation,
                             CreateSportSectionMutation,
                             CreateAchievementMutation)


class Query(AccountsQuery, SportQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    facebook_login = FacebookLoginMutation.Field()
    google_login = GoogleLoginMutation.Field()
    create_sport_category = CreateSportCategoryMutation.Field()
    create_sport_section = CreateSportSectionMutation.Field()
    create_achievement = CreateAchievementMutation.Field()
    update_user = UpdateUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
