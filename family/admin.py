from django.contrib import admin
from .models import Family

# Register your models here.

class FamilyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Family._meta.fields]

admin.site.register(Family, FamilyAdmin)