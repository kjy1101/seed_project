from django.contrib import admin
from .models import Seed, SeedImage

# Register your models here.

class SeedAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Seed._meta.fields]

class SeedImageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SeedImage._meta.fields]

admin.site.register(Seed, SeedAdmin)
admin.site.register(SeedImage, SeedImageAdmin)