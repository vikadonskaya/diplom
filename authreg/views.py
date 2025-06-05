from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, UserProfileForm
from django.contrib import messages


def reg(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешна! Теперь можно войти.')
            return redirect('auth')
    else:
        form = RegisterForm()
    return render(request, 'authreg/reg.html', {'form': form})


def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'authreg/auth.html')


def logout_view(request):
    logout(request)
    return redirect('auth')


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors)  # Вывод ошибок валидации

    else:
        form = UserProfileForm(instance=user)
    return render(request, 'user.html', {'form': form})
