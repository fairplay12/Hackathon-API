import graphene

from accounts.schema import Query as AccountsQuery
from accounts.mutations import (LoginMutation, RegisterMutation,
                                FacebookLoginMutation, GoogleLoginMutation,
                                UpdateUserMutation)
from sport.schema import Query as SportQuery
from sport.mutations import (CreateSportCategoryMutation,
                             CreateSportSectionMutation,
                             CreateAchievementMutation,
                             CreateCustomAchievementMutation,
                             CreateChampionshipMutation,
                             UpdateSportSectionMutation,
                             UpdateCustomAchievementMutation,
                             UpdateChampionshipMutation,
                             DeleteInstanceMutation, BecomeAnAthleteMutation)
from management.schema import Query as ManagementQuery
from management.mutations import (CreateReviewMutation,
                                  UpdateReviewMutation)


class Query(AccountsQuery, SportQuery, ManagementQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    facebook_login = FacebookLoginMutation.Field()
    google_login = GoogleLoginMutation.Field()
    create_sport_category = CreateSportCategoryMutation.Field()
    create_sport_section = CreateSportSectionMutation.Field()
    create_achievement = CreateAchievementMutation.Field()
    create_custom_achievement = CreateCustomAchievementMutation.Field()
    update_sport_section = UpdateSportSectionMutation.Field()
    update_custom_achievement = UpdateCustomAchievementMutation.Field()
    update_championship = UpdateChampionshipMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_instance = DeleteInstanceMutation.Field()
    become_an_athlete = BecomeAnAthleteMutation.Field()
    create_review = CreateReviewMutation.Field()
    update_review = UpdateReviewMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
