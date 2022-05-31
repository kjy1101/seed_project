from django.shortcuts import get_object_or_404, render, redirect
from .models import Seed
from .forms import SeedForm
# Create your views here.

def new(request):
    if request.method == 'POST': # POST 요청일때 새로운 seed 저장
        form = SeedForm(request.POST, request.FILES)
        if form.is_valid():
            seed = form.save(commit=False)
            seed.save()
            return redirect('home') # seed 생성 후 home 페이지로 리다이렉트
        else:
            print("form is invalid")

    else: # GET 요청일때 폼 작성
        form = SeedForm()
    
    return render(request, 'new.html', {'form':form})

def detail(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    return render(request, 'detail.html', {'seed':seed})

def edit(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    if request.method == "POST":
        form = SeedForm(request.POST, instance=seed)
        if form.is_valid():
            seed = form.save(commit=False)
            seed.save()
            return redirect('detail', pk=seed.pk)
        else:
            print("form is invalid")

    else:
        form = SeedForm(instance=seed)

    return render(request, 'edit.html', {'form':form, 'seed':seed})

def delete(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    seed.delete()
    return redirect('home')