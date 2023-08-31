from django.urls import path, include
from django.contrib.auth.views import LoginView


from .views import \
    get_cookie_view, \
    set_cookie_view, \
    get_session_view, \
    set_session_view, \
    MyLogoutView, \
    RegisterView, \
    AboutMe, \
    AvatarUpdateView, \
    ProfileListView, \
    ProfileDetailsView, \
    ProfileRegisterView, \
    ProfileDeleteView, \
    update_profile

app_name = 'accounts'


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("profiles/", ProfileListView.as_view(), name="profile_list"),
    path("profiles/create/", ProfileRegisterView.as_view(), name="profile_create"),
    path("profiles/<int:pk>/", ProfileDetailsView.as_view(), name="profile_detail"),
    path("about-me/", AboutMe.as_view(), name="about-me"),
    path("profiles/update_profile/", update_profile, name="profile_update"),
    path("profiles/avatar/<int:pk>/update/", AvatarUpdateView.as_view(), name="avatar_update"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
]
