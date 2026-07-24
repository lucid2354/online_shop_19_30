from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт успешно создан.')
        return redirect('catalog')
    return render(request, 'users/register.html', {'form': form})
