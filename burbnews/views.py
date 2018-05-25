from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
# from .models import
# from .forms import


@login_required(login_url='/accounts/login/')
def home(request, id):
    title = "Rider"
    current_user = request.user
    # profile = Rider_Profile.objects.get(name=current_user.id)
    context = {"title": title, "current_user": current_user, "profile": profile}

    return render(request, 'index-rider.html', context)


# @login_required(login_url='/accounts/login/')
# @transaction.atomic
# def edit_profile(request, id):
#     current_user = request.user
#     profile = Rider_Profile.objects.get(name=current_user.id)
#     if request.method == 'POST':
#         profile_form = EditProfile(request.POST, request.FILES, instance=current_user.profile)
#         user_form = EditUserForm(request.POST, instance=current_user)
#         if profile_form.is_valid() and user_form.is_valid():
#             profile = profile_form.save(commit=False)
#             user = user_form.save(commit=False)
#             profile.user = current_user
#             profile.save()
#             user.save()
#             return redirect('home', current_user.id)
#     else:
#         profile_form = EditProfile()
#         user_form = EditUserForm()
#
#     context = {
#         "current_user": current_user, "profile_form": profile_form,
#         "user_form": user_form, "profile": profile,
#         }
#     return render(request, 'edit-riderprofile.html', context)
