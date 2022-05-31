from django.shortcuts import get_object_or_404, render, redirect
from .models import Genus
from .forms import GenusForm
# Create your views here.

def new(request):
    if request.method == 'POST': # POST 요청일때 새로운 genus 저장
        if request.user.is_authenticated:
            form = GenusForm(request.POST, request.FILES)
            if form.is_valid():
                genus = form.save(commit=False)
                genus.save()
                return redirect('home') # genus 생성 후 home 페이지로 리다이렉트
            else:
                print("form is invalid")
        else:
            return render(request, 'new_g.html', {'error': 'login first'})

    else: # GET 요청일때 폼 작성
        form = GenusForm()
    
    return render(request, 'new_g.html', {'form':form})

def detail(request, pk):
    genus = get_object_or_404(Genus, pk=pk)
    return render(request, 'detail_g.html', {'genus':genus})

def edit(request, pk):
    genus = get_object_or_404(Genus, pk=pk)
    if request.method == "POST":
        form = GenusForm(request.POST, instance=genus)
        if form.is_valid():
            genus = form.save(commit=False)
            genus.save()
            return redirect('detail_g', pk=genus.pk)
        else:
            print("form is invalid")

    else:
        form = GenusForm(instance=genus)

    return render(request, 'edit_g.html', {'form':form, 'genus':genus})

def delete(request, pk):
    genus = get_object_or_404(Genus, pk=pk)
    genus.delete()
    return redirect('home')