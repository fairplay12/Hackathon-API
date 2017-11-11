import graphene
import base64

from django.core.files.base import ContentFile

from .schema import (SportSectionType, ChampionshipType,
                     CustomAchievementType)
from .models import (SportCategory, SportSection, Achievement,
                     Championship, CustomAchievement)
from accounts.models import User
from hackathon.decorators import login_required


class CreateSportCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        short_description = graphene.String()
        image = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        name = args.get('name')
        short_description = args.get('short_description')
        image = args.get('image')
        errors = []

        if not name:
            errors.append('Category name must be specified')

        if not short_description:
            errors.append('Description must be specified')

        if not image:
            errors.append('Image must be specified')

        if not errors:
            category = SportCategory.objects.create(**args)
            if image:
                img_format, img_str = image.split(';base64,')
                ext = img_format.split('/')['-1']
                image = ContentFile(base64.b64decode(
                    img_str), name=str(category.id) + ext)

                category.image = image

            category.save()

        return CreateSportCategoryMutation(errors=errors)


class CreateSportSectionMutation(graphene.Mutation):
    class Arguments:
        category_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        max_ppl_in_section = graphene.Int()
        image = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        category_id = args.get('category_id')
        name = args.get('name')
        description = args.get('description')
        max_ppl_in_section = args.get('max_ppl_in_section')
        image = args.get('image')
        errors = []

        if not category_id:
            errors.append('Section must have relation with category')

        if not name:
            errors.append('Name must be specified')

        if not description:
            errors.append('Description must be specified')

        if not max_ppl_in_section:
            errors.append('Max people in section must be specified')

        if not image:
            errors.append('Image must be specified')

        if not errors:
            user = info.context.user
            section = SportSection.objects.create(**args)
            user.sport_sections.add(section)
            user.is_trainer = True
            user.save()
            if image:
                img_format, img_str = image.split(';base64,')
                ext = img_format.split('/')['-1']
                image = ContentFile(base64.b64decode(
                    img_str), name=str(section.id) + ext)

                section.image = image
            section.save()

        return CreateSportSectionMutation(errors=errors)


class CreateAchievementMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID()
        name = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        user_id = args.get('user_id')
        name = args.get('name')
        errors = []

        if not user_id:
            errors.append('Achievement must have relation with user')

        if not name:
            errors.append('Name must be specified')

        if not errors:
            Achievement.objects.create(**args)

        return CreateAchievementMutation(errors=errors)


class CreateChampionshipMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        date = graphene.String()
        description = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        name = args.get('name')
        date = args.get('date')
        description = args.get('description')
        errors = []

        if not name:
            errors.append('Name must be specified')

        if not date:
            errors.append('Date must be specified')

        if not description:
            errors.append('Description must be specified')

        if not errors:
            Championship.objects.create(**args)

        return CreateChampionshipMutation(errors=errors)


class CreateCustomAchievementMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()
        name = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        section_id = args.get('section_id')
        name = args.get('name')
        errors = []

        if not section_id:
            errors.append('Custom achievement must have relation with Section')

        if not name:
            errors.append('Name must be specified')

        if not errors:
            CustomAchievement.objects.create(**args)

        return CreateCustomAchievementMutation(errors=errors)


class UpdateSportSectionMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        max_ppl_in_section = graphene.Int()

    errors = graphene.List(graphene.String)
    section = graphene.Field(lambda: SportSectionType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        section_id = args.get('section_id')
        name = args.get('name')
        description = args.get('description')
        max_ppl_in_section = args.get('max_ppl_in_section')
        errors = []
        section = None

        if not section_id:
            errors.append('Section id must be specified')

        if not name:
            errors.append('Name must be specified')

        if not description:
            errors.append('Description must be specified')

        if not max_ppl_in_section:
            errors.append('Max people must be specified')

        if not errors:
            try:
                section = SportSection.objects.get(pk=section_id)
            except SportSection.DoesNotExist:
                errors.append('That section doesn\'t exists')
                return UpdateSportSectionMutation(
                    errors=errors, section=section
                )

            section.name = name
            section.description = description
            section.max_ppl_in_section = max_ppl_in_section
            section.save

        return UpdateSportSectionMutation(errors=errors, section=section)


class UpdateChampionshipMutation(graphene.Mutation):
    class Arguments:
        championship_id = graphene.ID()
        name = graphene.String()
        date = graphene.String()
        description = graphene.String()

    errors = graphene.List(graphene.String)
    championship = graphene.Field(lambda: ChampionshipType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        championship_id = args.get('championship_id')
        name = args.get('name')
        date = args.get('date')
        description = args.get('description')
        errors = []
        championship = None

        if not championship_id:
            errors.append('Championship id must be specified')

        if not name:
            errors.append('Name must be specified')

        if not date:
            errors.append('Date must be specified')

        if not description:
            errors.append('Description must be specified')

        if not errors:
            try:
                championship = Championship.objects.get(pk=championship_id)
            except Championship.DoesNotExist:
                errors.append('That championship doesn\'t exists')
                return UpdateChampionshipMutation(
                    errors=errors,
                    championship=championship
                )

            championship.name = name
            championship.date = date
            championship.description = description
            championship.save()

        return UpdateChampionshipMutation(
            errors=errors, championship=championship
        )


class UpdateCustomAchievementMutation(graphene.Mutation):
    class Arguments:
        achievement_id = graphene.ID()
        name = graphene.String()

    errors = graphene.List(graphene.String)
    achievement = graphene.Field(lambda: CustomAchievementType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        achievement_id = args.get('achievement_id')
        name = args.get('name')
        errors = []
        achievement = None

        if not achievement_id:
            errors.append('Achievement id must be specified')

        if not name:
            errors.append('Name must be specified')

        if not errors:
            try:
                CustomAchievement.objects.get(pk=achievement_id)
            except CustomAchievement.DoesNotExist:
                errors.append('That achievement does\'t exists')
                return UpdateCustomAchievementMutation(
                    errors=errors,
                    achievement=achievement
                )

            achievement.name = name
            achievement.save()

        return UpdateCustomAchievementMutation(
            errors=errors,
            achievement=achievement
        )


class DeleteInstanceMutation(graphene.Mutation):
    class Arguments:
        instance_id = graphene.ID()
        instance_type = graphene.Int()

    errors = graphene.List(graphene.String)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        instance_id = args.get('instance_id')
        instance_type = args.get('instance_type')
        errors = []

        if not instance_id:
            errors.append('Instance id must be specified')

        if not instance_type:
            errors.append('Instance type must be specified')

        if not errors:
            if instance_type is 1:
                try:
                    User.objects.get(pk=instance_id).delete()
                except User.DoesNotExist:
                    errors.append('That user doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)
            elif instance_type is 2:
                try:
                    SportCategory.objects.get(pk=instance_id).delete()
                except SportCategory.DoesNotExist:
                    errors.append('That category doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)
            elif instance_type is 3:
                try:
                    SportSection.objects.get(pk=instance_id).delete()
                except SportSection.DoesNotExist:
                    errors.append('That section doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)
            elif instance_type is 4:
                try:
                    Achievement.objects.get(pk=instance_id).delete()
                except Achievement.DoesNotExist:
                    errors.append('That achievement doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)
            elif instance_type is 5:
                try:
                    CustomAchievement.objects.get(pk=instance_id).delete()
                except CustomAchievement.DoesNotExist:
                    errors.append('That achievement doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)
            elif instance_type is 6:
                try:
                    Championship.objects.get(pk=instance_id).delete()
                except Championship.DoesNotExist:
                    errors.append('That championship doesn\'t exists')
                    return DeleteInstanceMutation(errors=errors)

        return DeleteInstanceMutation(errors=errors)
