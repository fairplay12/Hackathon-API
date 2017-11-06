import graphene

from .schema import UserType
from .models import User
from hackathon.utils import obtain_jwt


class LoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    token = graphene.String()
    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, **args):
        email = args.get('email')
        password = args.get('password')
        errors = []
        user = None
        token = None

        if not email:
            errors.append("Email must be specified")

        if not password:
            errors.append("Password must be specified")

        if not errors:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    errors.append("Email or password is invalid")
                    user = None
                else:
                    token = obtain_jwt(user.id)
            except User.DoesNotExist:
                errors.append("Email or password is invalid")

        return LoginMutation(token=token, errors=errors, user=user)


class RegisterMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        email = args.get('email')
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        password = args.get('password')
        errors = []

        if not email:
            errors.append("Email must be specified")

        if not password:
            errors.append("Password must be specified")

        if not first_name:
            errors.append('First name must be specified')

        if not last_name:
            errors.append('Last name must be specified')

        if not errors:
            user = User.objects.create(**args)
            user.set_password(password)
            user.save()

        return RegisterMutation(errors=errors)
