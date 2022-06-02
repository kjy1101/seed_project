from django.shortcuts import get_object_or_404, render, redirect
from .models import Family
from .forms import FamilyForm
# Create your views here.

def new(request):
    if request.method == 'POST': # POST 요청일때 새로운 family 저장
        if request.user.is_authenticated:
            form = FamilyForm(request.POST, request.FILES)
            if form.is_valid():
                family = form.save(commit=False)
                family.user = request.user
                family.save()
                return redirect('/home') # family 생성 후 home 페이지로 리다이렉트
            else:
                print("form is invalid")
        else:
            return render(request, 'new_f.html', {'error': 'login first'})

    else: # GET 요청일때 폼 작성
        form = FamilyForm()
    
    return render(request, 'new_f.html', {'form':form})

def detail(request, pk):
    family = get_object_or_404(Family, pk=pk)
    return render(request, 'detail_f.html', {'family':family})

def edit(request, pk):
    family = get_object_or_404(Family, pk=pk)
    if request.method == "POST":
        form = FamilyForm(request.POST, instance=family)
        if form.is_valid():
            family = form.save(commit=False)
            family.save()
            return redirect('detail_f', pk=family.pk)
        else:
            print("form is invalid")

    else:
        form = FamilyForm(instance=family)

    return render(request, 'edit_f.html', {'form':form, 'family':family})

def delete(request, pk):
    family = get_object_or_404(Family, pk=pk)
    family.delete()
    return redirect('home')