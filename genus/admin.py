from django.contrib import admin
from .models import Genus

# Register your models here.

class GenusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Genus._meta.fields]

admin.site.register(Genus, GenusAdmin)