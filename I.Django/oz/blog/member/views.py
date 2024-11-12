from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login
from django.urls import reverse


# Create your views here.
def signup(request):
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    #
    # print(username,password1,password2)

    # username 중복확인작업
    # password 가 맞는지 ,그리고 정책에 올바른지(대소문자)

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
        next = request.GET.get('next')
        if next:
            return redirect(next)

        return redirect(reverse('blog_list'))

    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)