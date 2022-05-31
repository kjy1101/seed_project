from django.contrib import admin
from .models import Seed

# Register your models here.

class SeedAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Seed._meta.fields]

admin.site.register(Seed, SeedAdmin)