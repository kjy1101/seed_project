from django.shortcuts import get_object_or_404, render, redirect
from .models import Family
from .forms import FamilyForm
# Create your views here.

def new(request):
    if request.user.is_authenticated:
        if request.method == 'POST': # POST 요청일때 새로운 family 저장
            form = FamilyForm(request.POST, request.FILES)
            if form.is_valid():
                family = form.save(commit=False)
                family.user = request.user
                family.save()
                return redirect('home') # family 생성 후 home 페이지로 리다이렉트
            else:
                print("form is invalid")

        else: # GET 요청일때 폼 작성
            form = FamilyForm()

    else:
        return redirect('home') # 로그인 안했으면 홈으로
    
    return render(request, 'new_f.html', {'form':form})

def detail(request, pk):
    if request.user.is_authenticated:
        family = get_object_or_404(Family, pk=pk)
        return render(request, 'detail_f.html', {'family':family})
    else:
        return redirect('home') # 로그인 안했으면 홈으로

def edit(request, pk):
    if request.user.is_authenticated:
        family = get_object_or_404(Family, pk=pk)
        if request.user == family.user:
            if request.method == "POST":
                form = FamilyForm(request.POST, instance=family)
                if form.is_valid() and family.user == request.user:
                    family = form.save(commit=False)
                    family.save()
                    return redirect('detail_f', pk=family.pk)
                else:
                    print("form is invalid")

            else:
                form = FamilyForm(instance=family)
        else:
            print("Not your family")
            return redirect('home') # 내가 만든거 아니면 홈으로
    else:
        print("Not authenticated")
        return redirect('home') # 로그인 안했으면 홈으로

    return render(request, 'edit_f.html', {'form':form, 'family':family})

def delete(request, pk):
    if request.user.is_authenticated:
        family = get_object_or_404(Family, pk=pk)
        if family.user == request.user:
            family.delete()
        else:
            print("Not your family")
    else:
        print("Not authenticated")
        
    return redirect('home')