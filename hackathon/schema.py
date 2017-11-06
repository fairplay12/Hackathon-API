import graphene

from accounts.schema import Query as AccountsQuery
from accounts.mutations import LoginMutation, RegisterMutation


class Query(AccountsQuery, RegisterMutation, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
