from django.urls import path

from apps.users import views as users_views

urlpatterns = [
    path("verify/<str:token>", users_views.UserCreate.as_view(), name='user_verify'),
]
