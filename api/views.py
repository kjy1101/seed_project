from django.contrib import auth
from django.contrib.auth import get_user_model, authenticate
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters.rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from io import BytesIO
from django.http import HttpResponse
import csv, os
from rest_framework.viewsets import ModelViewSet

from seed_project.settings import SECRET_KEY
from seed.models import Seed, SeedImage
from family.models import Family
from genus.models import Genus
from PIL import Image
from django.core.files.base import ContentFile
from .serializer import SeedSerializer, FamilySerializer, GenusSerializer, SeedImageSerializer
from django.shortcuts import redirect, render


# 파일 : seed_info.csv
# row[0] : 도입번호
# row[1] : 과명
# row[2] : 과국명
# row[3] : 속명
# row[4] : 속국명
# row[5] : 도입학명
# row[6] : 국명
# row[7] : 현미경(단립, 복립)
# row[8] : 종자길이(mm)
# row[9] : 종자너비(mm)
# row[10] : 비고


# (csv->DB) 과명/과국명, 속명/속국명 저장
def save_family_genus_info(request):
    f_path = os.path.abspath(os.path.join(
        'seed_info.csv'
    ))

    with open(f_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)  # 제일 윗줄 제외
        for row in reader:
            print(row[1], row[2], row[3], row[4])
            Family.objects.get_or_create(
                family_en=row[1],
                family_ko=row[2]
            )
            Genus.objects.get_or_create(
                genus_en=row[3],
                genus_ko=row[4]
            )

    return HttpResponse("family & genus info upload")


# (csv->DB) 종자 정보 저장
def save_seed_info(request):
    f_path = os.path.abspath(os.path.join(
        'seed_info.csv'
    ))

    with open(f_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)  # 제일 윗줄 제외
        for row in reader:
            print(row[0], row[5], row[6], row[7], row[8], row[9], row[10])

            # 과명/과국명
            family = Family.objects.get(family_en=row[1], family_ko=row[2])

            # 속명/속국명
            genus = Genus.objects.get(genus_en=row[3], genus_ko=row[4])

            # 현미경(단립, 복립)
            if row[7] == "O":
                microscope = True
            else:
                microscope = False

            # 종자길이/종자길이오차
            if "±" in row[8]:
                sl = row[8].split("±")
                seed_length = float(sl[0])
                seed_length_error = float(sl[1])
            else:
                seed_length = None
                seed_length_error = None

            # 종자너비/종자너비오차
            if "±" in row[9]:
                sw = row[9].split("±")
                seed_width = float(sw[0])
                seed_width_error = float(sw[1])
            else:
                seed_width = None
                seed_width_error = None

            # 씨앗 생성
            Seed.objects.get_or_create(
                intro_num=row[0],  # 도입번호
                family=family,  # 과명/과국명
                genus=genus,  # 속명/속국명
                used_scientific_name=row[5],  # 도입학명
                plant_name=row[6],  # 국명
                microscope=microscope,  # 현미경(단립, 복립)
                seed_length=seed_length,  # 종자길이
                seed_length_error=seed_length_error,  # 종자길이오차
                seed_width=seed_width,  # 종자너비
                seed_width_error=seed_width_error,  # 종자너비오차
                note=row[10],  # 비고
            )

    # 기타 씨앗 생성
    Seed.objects.get_or_create(
        intro_num="0000-0000",
        plant_name="기타"
    )

    return HttpResponse("seed info upload")


# 종자 이미지 업로드
def save_images(request):
    root_dir = os.path.abspath(os.path.join(
        "현미경5차"
    ))

    root_folder_list = os.listdir(root_dir)
    for i, root_folder in enumerate(root_folder_list, start=0):
        if i == 0:
            continue
        root_folder_path = root_dir + "/" + root_folder
        print(root_folder_path)

        if i in [1, 4, 5]:  # 폴더 > 파일
            file_list = os.listdir(root_folder_path)
            for file in file_list:
                # print("- ", file)
                intro_num = file.replace("_", " ").split(" ")[0]  # 도입번호 잘라내기
                f_path = root_folder_path + "/" + file  # 이미지 파일 최종 경로

                # 이미지 만들기
                image = Image.open(f_path)  # 이미지 파일 열기
                image = image.convert("RGB")
                image_io = BytesIO()
                image.save(image_io, format="JPEG", quality=100)
                image_content = ContentFile(image_io.getvalue(), file)

                # 씨앗 종자 객체에 넣기
                try:
                    seed = Seed.objects.get(intro_num=intro_num)

                except Seed.DoesNotExist:  # 도입번호로 종자 못찾음 => 기타
                    seed = Seed.objects.get(intro_num="0000-0000")

                # 씨앗 종자 이미지 모델 만들기
                SeedImage.objects.get_or_create(
                    seed=seed,
                    image=image_content
                )

        else:  # 폴더 > 폴더 > 파일
            folder_list = os.listdir(root_folder_path)
            for folder in folder_list:
                folder_path = root_folder_path + "/" + folder  # 이미지 파일 최종 경로
                # print(folder_path)

                file_list = os.listdir(folder_path)

                for file in file_list:
                    # print("- ", file)
                    intro_num = file.replace('_', ' ').split(' ')[0]
                    f_path = folder_path + "/" + file

                    # 이미지 만들기
                    image = Image.open(f_path)  # 이미지 파일 열기
                    image = image.convert("RGB")
                    image_io = BytesIO()
                    image.save(image_io, format="JPEG", quality=100)
                    image_content = ContentFile(image_io.getvalue(), file)

                    # 씨앗 종자 객체에 넣기
                    try:
                        seed = Seed.objects.get(intro_num=intro_num)

                    except Seed.DoesNotExist:  # 도입번호로 종자 못찾음 => 기타
                        seed = Seed.objects.get(intro_num="0000-0000")

                    # 씨앗 종자 이미지 모델 만들기
                    SeedImage.objects.get_or_create(
                        seed=seed,
                        image=image_content
                    )

    return HttpResponse("image upload")


class SeedFilter(FilterSet):
    intro_num = filters.CharFilter(field_name='intro_num', lookup_expr="icontains")
    used_scientific_name = filters.CharFilter(field_name='used_scientific_name', lookup_expr="icontains")
    plant_name = filters.CharFilter(field_name='plant_name', lookup_expr="icontains")
    family_en = filters.CharFilter(method='filter_family_en', lookup_expr="icontains")
    family_ko = filters.CharFilter(method='filter_family_ko', lookup_expr="icontains")
    genus_en = filters.CharFilter(method='filter_genus_en', lookup_expr="icontains")
    genus_ko = filters.CharFilter(method='filter_genus_ko', lookup_expr="icontains")

    class Meta:
        model = Seed
        fields = ['intro_num', 'used_scientific_name', 'plant_name', 'family_en', 'family_ko', 'genus_en', 'genus_ko']

    def filter_family_en(self, queryset, name, value):
        family = Family.objects.get(family_en__contains=value)
        filtered_queryset = queryset.filter(family=family)
        return filtered_queryset

    def filter_family_ko(self, queryset, name, value):
        family = Family.objects.get(family_ko__icontains=value)
        filtered_queryset = queryset.filter(family=family)
        return filtered_queryset

    def filter_genus_en(self, queryset, name, value):
        genus = Genus.objects.get(genus_en__icontains=value)
        filtered_queryset = queryset.filter(genus=genus)
        return filtered_queryset

    def filter_genus_ko(self, queryset, name, value):
        genus = Genus.objects.get(genus_ko__icontains=value)
        filtered_queryset = queryset.filter(genus=genus)
        return filtered_queryset


class SeedViewSet(ModelViewSet):
    serializer_class = SeedSerializer
    queryset = Seed.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SeedFilter

    # def perform_create(self, serializer):  # 생성
    #     data = self.request.data
    #     # instance, check = Seed.objects.get_or_create(
    #     instance = serializer.save(
    #         intro_num=data.get('intro_num'),
    #         family_id=data.get('family'),
    #         genus_id=data.get('genus'),
    #         used_scientific_name=data.get('used_scientific_name'),
    #         plant_name=data.get('plant_name'),
    #         microscope=data.get('microscope'),
    #         seed_length=data.get('seed_length'),
    #         seed_width=data.get('seed_width'),
    #         seed_width_error=data.get('seed_width_error'),
    #         seed_length_error=data.get('seed_length_error'),
    #         note=data.get('note')
    #     )
    #     print("views에서 생성")
    #     image_set = self.request.FILES
    #     # print(image_set)
    #     # print(serializer)
    #     # print(serializer.validated_data.get('id'))
    #     # print(id.id)
    #     # print("instance:", instance)
    #     for image_data in image_set.getlist('image'):
    #         SeedImage.objects.create(seed=instance, image=image_data)
    #         # print(image_data)
    #     return super().perform_create(serializer)

    # def post(self, request, pk):  # 수정
    #     data = self.request.data
    #     print("수정된 데이터: ", data)
    #     seed = Seed.objects.get(pk=pk)
    #     seed.intro_num = data.get('intro_num')
    #     seed.family_id = data.get('family')
    #     seed.genus_id = data.get('genus')
    #     seed.used_scientific_name = data.get('used_scientific_name')
    #     seed.plant_name = data.get('plant_name')
    #     seed.microscope = data.get('microscope')
    #     seed.seed_length = data.get('seed_length')
    #     seed.seed_width = data.get('seed_width')
    #     seed.seed_width_error = data.get('seed_width_error')
    #     seed.seed_length_error = data.get('seed_length_error')
    #     seed.note = data.get('note')
    #     seed.save()
    #
    #     # 기존 이미지 수정
    #     for s in seed.images.all():
    #         # print(s)
    #         # print(s.id)
    #         origin_image_str = "origin_image" + str(s.id)
    #         origin_image = data.get(origin_image_str)
    #         print("origin image: ", origin_image)
    #         if origin_image == None:
    #             print("삭제됨")
    #             deleted_image = SeedImage.objects.get(pk=s.id)
    #             deleted_image.delete()
    #         else:
    #             print("그대로 유지")
    #
    #     # 새 이미지 추가
    #     image_set = self.request.FILES
    #     # print(image_set)
    #     for image_data in image_set.getlist('image'):
    #         SeedImage.objects.create(seed=seed, image=image_data)
    #         print(image_data)
    #
    #     redirect_url = 'http://localhost:8000/app/seeds/' + str(seed.id)
    #     return redirect(redirect_url)


class FamilyViewSet(ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()


class GenusViewSet(ModelViewSet):
    serializer_class = GenusSerializer
    queryset = Genus.objects.all()
