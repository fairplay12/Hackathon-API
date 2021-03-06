import graphene

from .models import Review, Training
from .schema import ReviewType, TrainingType
from hackathon.decorators import login_required


class CreateReviewMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()
        text = graphene.String()
        score = graphene.Int()

    errors = graphene.List(graphene.String)
    review = graphene.Field(lambda: ReviewType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        section_id = args.get('section_id')
        text = args.get('text')
        score = args.get('score')
        errors = []
        review = None

        if not section_id:
            errors.append('Section id must be specified')

        if not text:
            errors.append('Text must be specified')

        if not score:
            errors.append('Score must be specified')

        if not errors:
            args['user'] = info.context.user
            review = Review.objects.create(**args)

        return CreateReviewMutation(errors=errors, review=review)


class UpdateReviewMutation(graphene.Mutation):
    class Arguments:
        review_id = graphene.ID()
        text = graphene.String()
        score = graphene.Int()

    errors = graphene.List(graphene.String)
    review = graphene.Field(lambda: ReviewType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        review_id = args.get('review_id')
        text = args.get('text')
        score = args.get('score')
        errors = []
        review = None

        if not review_id:
            errors.append('Review id must be specified')

        if not text:
            errors.append('Text must be specified')

        if not score:
            errors.append('Score must be specified')

        if not errors:
            try:
                review = Review.objects.get(pk=review_id)
            except Review.DoesNotExist:
                errors.append('That review doesn\'t exists')
                return UpdateReviewMutation(
                    errors=errors,
                    review=review
                )
            review.text = text
            review.score = score
            review.save()

        return UpdateReviewMutation(errors=errors, review=review)


class CreateTrainingMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()
        day = graphene.Int()

    errors = graphene.List(graphene.String)
    training = graphene.Field(lambda: TrainingType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        section_id = args.get('section_id')
        day = args.get('day')
        errors = []
        training = None

        if not section_id:
            errors.append('Section id must be specified')

        if not day:
            errors.append('Day must be specified')

        if not errors:
            training = Training.objects.create(**args)

        return CreateTrainingMutation(
            errors=errors,
            training=training
        )
