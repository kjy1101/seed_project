from django.shortcuts import render
from seed.models import Seed
from family.models import Family
from genus.models import Genus

# Create your views here.

def home(request):
    seed = Seed.objects.all()
    family = Family.objects.all()
    genus = Genus.objects.all()
    return render(request, 'home.html', {'seed_list':seed, 'family_list':family, 'genus_list':genus})