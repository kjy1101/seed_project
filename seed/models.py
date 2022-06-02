from django.db import models
import os

# Create your models here.

def image_upload_path(instance, filename):
    if instance.seed.intro_num == "0000-0000" or instance.seed.intro_num == None:
        upload_path = os.path.join("image", "기타", filename)
    else:
        upload_path = os.path.join("image", instance.seed.family.family_ko, instance.seed.genus.genus_ko, filename) # 파일경로 : image\국화과\참취속\2020-001492 좀개미취 단립.jpg
    print(upload_path)
    return upload_path

class Seed(models.Model):
    intro_num = models.CharField(max_length=40, null=True, blank=True, help_text="도입번호")
    family = models.ForeignKey("family.Family", related_name="family", on_delete=models.CASCADE, null=True, blank=True, help_text="과명/과국명")
    genus = models.ForeignKey("genus.Genus", related_name="genus", on_delete=models.CASCADE, null=True, blank=True, help_text="속명/속국명")
    used_scientific_name = models.CharField(max_length=100, null=True, blank=True, help_text="도입학명")
    plant_name = models.CharField(max_length=40, null=True, blank=True, help_text="국명")
    microscope = models.BooleanField(default=True, null=True, blank=True, help_text="현미경(단립, 복립)")
    seed_length = models.FloatField(null=True, blank=True, help_text="종자길이(mm)")
    seed_length_error = models.FloatField(null=True, blank=True, help_text="종자길이오차")
    seed_width = models.FloatField(null=True, blank=True, help_text="종자너비(mm)")
    seed_width_error = models.FloatField(null=True, blank=True, help_text="종자너비오차")
    note = models.TextField(null=True, blank=True, help_text="비고")
    user = models.ForeignKey("main.User", related_name="user", on_delete=models.CASCADE)

    def __str__(self):
        return self.plant_name

class SeedImage(models.Model):
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True, help_text="이미지")

    def __str__(self):
        return "aaa"