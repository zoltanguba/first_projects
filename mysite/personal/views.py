from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import (UserLoginForm,
                    UserRegisterForm,
                    UserUpdateForm)
from translate import forms as translate_forms
from translate import models as translate_models


def index(request):
    return render(request, 'personal/index.html')


def user_login(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:  # This redirects the user from the login page to the page they wanted to visit without being authenticated
            return redirect(next)
        return redirect('contentlist')

    return render(request, 'personal/user_login.html', {'form': form})


def user_register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        translate_models.DestinationLanguage.objects.create(
            destLanguage='EN',
            user=request.user
        )
        return redirect('contentlist')

    #context = {"form": form}

    return render(request, 'personal/user_register.html', {"form": form})


def user_profile(request, pk):
    user = request.user
    destLanguage = translate_models.DestinationLanguage.objects.filter(user=user)  #.values('destLanguage')[0]['destLanguage']

    #  Delete below ///////////////////////////////////
    if destLanguage:
        pass
    else:
        translate_models.DestinationLanguage.objects.create(
            destLanguage='EN',
            user=request.user
        )
    #  Delete above ///////////////////////////////////

    instance = get_object_or_404(translate_models.DestinationLanguage, user=pk)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        language_form = translate_forms.DestinationLanguageForm(request.POST, instance=instance)
        if user_form.is_valid() and language_form.is_valid():
            user_form.save()
            language_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('contentlist')

    else:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        language_form = translate_forms.DestinationLanguageForm(request.POST, instance=instance)

    context = {
        'user_form': user_form,
        'language_form': language_form,
        'destLanguage': destLanguage
    }

    return render(request, 'personal/user_profile.html', context)




def user_logout(request):
    logout(request)
    return render(request, 'personal/base.html', {})
