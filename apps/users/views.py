from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.users.models import User, Santa


class UserCreate(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        try:
            user = User.objects.get(token=token)
            try:
                Santa.objects.get(santa=user)
            except Santa.DoesNotExist:
                random_user = User.objects.filter(selected=False).exclude(id=user.id).order_by("?").first()
                if not random_user:
                    random_user = User.objects.exclude(id=user.id).order_by("?").first()
                Santa.objects.create(santa=user, user=random_user)
                random_user.selected = True
                random_user.save()
            user.verified = True
            user.token = None
            user.save()
            print(f'User {user.name} verified!')
            return HttpResponse('<h1>You are in!</h1>')
        except User.DoesNotExist:
            print('User with this token does not exists!')
            return HttpResponse('<h1>O_o, some troubles, call support!</h1>')
