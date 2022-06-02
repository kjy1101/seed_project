from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from main.models import User
from seed.models import Seed
from family.models import Family
from genus.models import Genus

# Create your views here.

def home(request):
    seed = Seed.objects.all()
    family = Family.objects.all()
    genus = Genus.objects.all()
    return render(request, 'home.html', {'seed_list':seed, 'family_list':family, 'genus_list':genus})


def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(
                                        organization=request.POST['organization'],
                                        login_id=request.POST['login_id'],
                                        password=request.POST['password'],
                                        email=request.POST['email'],
                                        name=request.POST['name']
        )
        auth.login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

# 로그인
def login(request):
    if request.method == 'POST':
        print(request.user)
        login_id = request.POST['login_id']
        password = request.POST['password']
        user = authenticate(request, login_id=login_id, password=password)
        if user is not None:
            auth.login(request, user)
            print(request.user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


# 로그아웃
def logout(request):
    print(request.user)
    auth.logout(request)
    return redirect('login')
