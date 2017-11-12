import graphene
import facebook
import requests
import json
import base64

from django.core.files.base import ContentFile

from .schema import UserType
from .models import User, SocialAssociation
from hackathon.utils import obtain_jwt
from hackathon.decorators import login_required


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
            username = "{}{}".format(first_name.lower(), last_name.lower())
            args['username'] = username
            user = User.objects.create(**args)
            user.set_password(password)
            user.save()

        return RegisterMutation(errors=errors)


class FacebookLoginMutation(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()

    token = graphene.String()
    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, **args):
        access_token = args.get('access_token')
        token = None
        user = None
        errors = []

        if not access_token:
            errors.append("Access token must be specified")

        if not errors:
            try:
                graph = facebook.GraphAPI(
                    access_token=access_token,
                    version='2.7'
                )
                data = graph.get_object(
                    id='me',
                    fields='first_name,last_name,email'
                )
                try:
                    social_account = SocialAssociation.objects.get(
                        social_id=data.get('id')
                    )
                    user = social_account.user
                    token = obtain_jwt(user.id)

                except SocialAssociation.DoesNotExist:
                    try:
                        user = User.objects.get(
                            email=data.get('email')
                        )
                    except User.DoesNotExist:
                        user = User.objects.create(
                            email=data.get('email'),
                            first_name=data.get('first_name'),
                            last_name=data.get('last_name'),
                            username=data.get('email').split('@')[0]
                        )

                    social_account = SocialAssociation.objects.create(
                        social_id=data.get('id'),
                        user=user,
                        social_network='facebook'
                    )

                    token = obtain_jwt(user.id)

            except facebook.GraphAPIError:
                errors.append("Invalid access token")

        return FacebookLoginMutation(token=token, errors=errors, user=user)


class GoogleLoginMutation(graphene.Mutation):
    class Arguments:
        access_token = graphene.String()

    token = graphene.String()
    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, **args):
        access_token = args.get('access_token')
        token = None
        user = None
        errors = []

        if not access_token:
            errors.append("Access token must be specified")

        if not errors:
            response = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s" %
                access_token
            )
            if response.status_code == 200:
                data = json.loads(response.text)

                try:
                    social_account = SocialAssociation.objects.get(
                        social_id=data.get('id')
                    )
                    user = social_account.user
                    token = obtain_jwt(user.id)

                except SocialAssociation.DoesNotExist:
                    try:
                        user = User.objects.get(
                            email=data.get('email')
                        )
                    except User.DoesNotExist:
                        user = User.objects.create(
                            email=data.get('email'),
                            first_name=data.get('first_name'),
                            last_name=data.get('last_name'),
                            username=data.get('email').split('@')[0]
                        )

                    social_account = SocialAssociation.objects.create(
                        social_id=data.get('id'),
                        user=user,
                        social_network='google'
                    )

                    token = obtain_jwt(user.id)
            elif response.status_code == 401:
                errors.append("Invalid access token")

        return GoogleLoginMutation(token=token, errors=errors, user=user)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        expirience = graphene.Int()
        username = graphene.String()
        email = graphene.String()
        about = graphene.String()
        phone = graphene.String()
        avatar = graphene.String()

    errors = graphene.List(graphene.String)
    user = graphene.Field(lambda: UserType)

    @staticmethod
    @login_required
    def mutate(root, info, **args):
        user_id = args.get('user_id')
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        expirience = args.get('expirience')
        username = args.get('username')
        email = args.get('email')
        about = args.get('about')
        phone = args.get('phone')
        avatar = args.get('avatar')
        errors = []
        user = None

        if not user_id:
            errors.append('User id must be specified')

        if not first_name:
            errors.append('First name must be specified')

        if not last_name:
            errors.append('Last name must be specified')

        if not expirience:
            errors.append('Expirience must be specified')

        if not username:
            errors.append('Username must be specified')

        if not email:
            errors.append('Email must be specified')

        if not about:
            errors.append('About must be specified')

        if not phone:
            errors.append('Phone must be specified')

        if not avatar:
            errors.append('Avatar must be specified')

        if not errors:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                errors.append('That user doesn\'t exists')
                return UpdateUserMutation(errors=errors, user=user)

            user.first_name = first_name
            user.last_name = last_name
            user.expirience = expirience
            user.username = username
            user.email = email
            user.about = about
            user.phone = phone

            if avatar:
                img_format, img_str = avatar.split(';base64,')
                ext = img_format.split('/')['-1']
                avatar = ContentFile(base64.b64decode(
                    img_str), name=str(user.id) + ext)

                user.avatar = avatar

            user.save()

        return UpdateUserMutation(errors=errors, user=user)
