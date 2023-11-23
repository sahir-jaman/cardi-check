from django.urls import path


from ..views.users import PrivateUserList

urlpatterns = [
    path("", PrivateUserList.as_view(), name="user.list"),
]
