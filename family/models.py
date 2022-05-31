from django.db import models


class Family(models.Model):
    id = models.AutoField(primary_key=True)
    family_en = models.CharField(max_length=40, null=True, blank=True, help_text="과명")
    family_ko = models.CharField(max_length=40, null=True, blank=True, help_text="과국명")
    user = models.ForeignKey("main.User", related_name="family_user", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.family_ko