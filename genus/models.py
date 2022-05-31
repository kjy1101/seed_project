from django.db import models

# Create your models here.

class Genus(models.Model):
    id = models.AutoField(primary_key=True)
    genus_en = models.CharField(max_length=40, null=True, blank=True, help_text="속명")
    genus_ko = models.CharField(max_length=40, null=True, blank=True, help_text="속국명")

    def __str__(self):
        return self.genus_ko