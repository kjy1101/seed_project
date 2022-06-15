from django.urls import path, include

from api.views import save_family_genus_info, save_seed_info, save_images
from api.views import SeedViewSet, FamilyViewSet, GenusViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'seeds', SeedViewSet)
router.register(r'family', FamilyViewSet)
router.register(r'genus', GenusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('save_family_genus_info', save_family_genus_info), # 과명/속명 업로드
    path('save_seed_info', save_seed_info), # 종자정보 업로드
    path('save_images', save_images), # 이미지 업로드
]