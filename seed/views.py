from django.shortcuts import get_object_or_404, render, redirect
from .models import Seed, SeedImage
from .forms import SeedForm


# Create your views here.

def new(request):
    if request.method == 'POST':  # POST 요청일때 새로운 seed 저장
        if request.user.is_authenticated:
            form = SeedForm(request.POST)
            if form.is_valid():
                # 종자 생성
                seed = form.save(commit=False)
                seed.user = request.user
                seed.save()

                # 이미지 생성
                image_set = request.FILES
                for image_data in image_set.getlist('image'):
                    SeedImage.objects.create(seed=seed, image=image_data)

                return redirect('home')  # seed 생성 후 home 페이지로 리다이렉트
            else:
                print("form is invalid")
        else:
            return render(request, 'new.html', {'error': 'login first'})

    else:  # GET 요청일때 폼 작성
        form = SeedForm()

    return render(request, 'new.html', {'form': form})


def detail(request, pk):
    if request.user.is_authenticated:
        seed = get_object_or_404(Seed, pk=pk)
        print(seed.grain)
        return render(request, 'detail.html', {'seed': seed})


def edit(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    if request.method == "POST" and request.user.is_authenticated:
        form = SeedForm(request.POST, instance=seed)
        if form.is_valid() and seed.user == request.user:
            seed = form.save(commit=False)
            seed.save()

            # 기존 이미지 수정
            for s in seed.images.all():
                origin_image_str = "origin_image" + str(s.id)
                origin_image = form.data.get(origin_image_str)
                if origin_image == None:
                    print("삭제됨")
                    deleted_image = SeedImage.objects.get(pk=s.id)
                    deleted_image.delete()
                else:
                    print("그대로 유지")

            # 이미지 추가
            image_set = request.FILES
            for image_data in image_set.getlist('image'):
                SeedImage.objects.create(seed=seed, image=image_data)

            return redirect('detail', pk=seed.pk)
        else:
            print("form is invalid")

    else:
        form = SeedForm(instance=seed)

    return render(request, 'edit.html', {'form': form, 'seed': seed})


def delete(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    if seed.user == request.user:
        seed.delete()
        return redirect('home')
