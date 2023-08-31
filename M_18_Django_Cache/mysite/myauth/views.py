from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .forms import UserForm, ProfileForm
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class AboutMe(TemplateView):
    template_name = "myauth/about-me.html"


class ProfileListView(ListView):
    queryset = (
        Profile.objects.select_related("user")
    )


class ProfileDetailsView(DetailView):
    queryset = (
        Profile.objects.select_related("user")
    )


class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_staff\
                or self.request.user.profile.pk == self.get_object().pk:
            return True
        else:
            return False

    model = Profile
    fields = "avatar",
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "accounts:profile_detail",
            kwargs={"pk": self.object.pk}
        )


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("accounts:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileRegisterView(CreateView):
    model = Profile
    fields = "bio", "avatar",
    success_url = reverse_lazy("accounts:about-me")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.is_superuser

    model = Profile
    success_url = reverse_lazy("accounts:profile_list")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:about-me')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'myauth/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })