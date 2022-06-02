from django.contrib import auth
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, redirect

from main.models import User
from seed.models import Seed
from family.models import Family
from genus.models import Genus

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        seed = Seed.objects.all()
        family = Family.objects.all()
        genus = Genus.objects.all()
        return render(request, 'home.html', {'seed_list':seed, 'family_list':family, 'genus_list':genus})
    else:
        return redirect('login')


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
    return redirect('home')

def search(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            intro_num = request.POST.get('intro_num')
            family_en = request.POST.get('family_en')
            family_ko = request.POST.get('family_ko')
            genus_en = request.POST.get('genus_en')
            genus_ko = request.POST.get('genus_ko')
            used_scientific_name = request.POST.get('used_scientific_name')
            plant_name = request.POST.get('plant_name')
            q = Q()

            if intro_num != '':
                q &= Q(intro_num__icontains=intro_num)
            if family_en != '':
                q &= Q(family__family_en__icontains=family_en)
            if family_ko != '':
                q &= Q(family__family_ko__icontains=family_ko)
            if genus_en != '':
                q &= Q(genus__genus_en__icontains=genus_en)
            if genus_ko != '':
                q &= Q(genus__genus_ko__icontains=genus_ko)
            if used_scientific_name != '':
                q &= Q(used_scientific_name__icontains=used_scientific_name)
            if plant_name != '':
                q &= Q(plant_name__icontains=plant_name)
            seeds = Seed.objects.filter(q)
            return render(request, 'result.html', {'seed_list':seeds,})
    else:
        return render(request, 'search.html')
