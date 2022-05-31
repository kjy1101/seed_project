from django.db import models

# Create your models here.

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