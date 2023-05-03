from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import ProfileEditForm, UserEditForm
from .forms import UserRegistrationForm
from .models import Profile
from NewsApp.models import News


# Create your views here.
def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user,
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form": user_form,
        }
        return render(request, 'account/register.html', context)


def dashboard_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    news = News.objects.filter(user=user)
    context = {
        "user": user,
        "profile": profile_info,
        "news": news
    }
    return render(request, 'pages/user_profile.html', context)


def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'account/profile_edit.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_user,
    }
    return render(request, 'pages/admin_page.html', context)
