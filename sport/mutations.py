import graphene

from .schema import (SportCategoryType, SportSectionType,
                     AchievementType, ChampionshipType)
from .models import (SportCategory, SportSection, Achievement,
                     Championship)


class CreateSportCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        short_description = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        name = args.get('name')
        short_description = args.get('short_description')
        errors = []

        if not name:
            errors.append('Category name must be specified')

        if not short_description:
            errors.append('Description must be specified')

        if not errors:
            SportCategory.objects.create(**args)

        return CreateSportCategoryMutation(errors=errors)


class CreateSportSectionMutation(graphene.Mutation):
    class Arguments:
        category_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        max_ppl_in_section = graphene.Int()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        category_id = args.get('category_id')
        name = args.get('name')
        description = args.get('description')
        max_ppl_in_section = args.get('max_ppl_in_section')
        errors = []

        if not category_id:
            errors.append('Section must have relation with category')

        if not name:
            errors.append('Name must be specified')

        if not description:
            errors.append('Description must be specified')

        if not max_ppl_in_section:
            errors.append('Max people in section must be specified')

        if not errors:
            SportSection.objects.create(**args)

        return CreateSportSectionMutation(errors=errors)
