from django.shortcuts import get_object_or_404, render, redirect
from .models import Genus
from .forms import GenusForm
# Create your views here.

def new(request):
    if request.user.is_authenticated:
        if request.method == 'POST': # POST 요청일때 새로운 genus 저장
            form = GenusForm(request.POST, request.FILES)
            if form.is_valid():
                genus = form.save(commit=False)
                genus.user = request.user
                genus.save()
                return redirect('home') # genus 생성 후 home 페이지로 리다이렉트
            else:
                print("form is invalid")

        else: # GET 요청일때 폼 작성
            form = GenusForm()

    else:
        return redirect('home') # 로그인 안했으면 홈으로
    
    return render(request, 'new_g.html', {'form':form})

def detail(request, pk):
    if request.user.is_authenticated:
        genus = get_object_or_404(Genus, pk=pk)
        return render(request, 'detail_g.html', {'genus':genus})
    else:
        return redirect('home') # 로그인 안했으면 홈으로

def edit(request, pk):
    if request.user.is_authenticated:
        genus = get_object_or_404(Genus, pk=pk)
        if request.user == genus.user:
            if request.method == "POST":
                form = GenusForm(request.POST, instance=genus)
                if form.is_valid() and genus.user==request.user:
                    genus = form.save(commit=False)
                    genus.save()
                    return redirect('detail_g', pk=genus.pk)
                else:
                    print("form is invalid")

            else:
                form = GenusForm(instance=genus)
        else:
            print("Not your genus")
            return redirect('home') # 내가 만든거 아니면 홈으로
    else:
        print("Not authenticated")
        return redirect('home') # 로그인 안했으면 홈으로

    return render(request, 'edit_g.html', {'form':form, 'genus':genus})

def delete(request, pk):
    if request.user.is_authenticated:
        genus = get_object_or_404(Genus, pk=pk)
        if genus.user == request.user:
            genus.delete()
            return redirect('home')
        else:
            print("Not your genus")
    else:
        print("Not authenticated")
        
    return redirect('home')