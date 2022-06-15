from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import serializers
from seed.models import Seed, SeedImage
from family.models import Family
from genus.models import Genus


class SeedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeedImage
        fields = ['image']


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['url', 'id', 'family_en', 'family_ko']


class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = ['url', 'id', 'genus_en', 'genus_ko']


class SeedSerializer(serializers.ModelSerializer):
    # images = SeedImageSerializer(many=True, read_only=True)

    class Meta:
        model = Seed
        fields = ['url', 'id', 'intro_num', 'used_scientific_name', 'plant_name', 'microscope', 'seed_length',
                  'seed_length_error',
                  'seed_width', 'seed_width_error', 'note', 'images', 'family', 'genus']

    def create(self, validated_data):
        data = self.context['request'].data
        instance, check = Seed.objects.get_or_create(
            intro_num=data.get('intro_num'),
            family_id=data.get('family'),
            genus_id=data.get('genus'),
            used_scientific_name=data.get('used_scientific_name'),
            plant_name=data.get('plant_name'),
            microscope=data.get('microscope'),
            seed_length=data.get('seed_length'),
            seed_width=data.get('seed_width'),
            seed_width_error=data.get('seed_width_error'),
            seed_length_error=data.get('seed_length_error'),
            note=data.get('note')
        )
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            SeedImage.objects.create(seed=instance, image=image_data)
        return instance

    def to_representation(self, instance):
        self.fields['family'] = FamilySerializer()
        self.fields['genus'] = GenusSerializer()
        self.fields['images'] = SeedImageSerializer(many=True)
        return super(SeedSerializer, self).to_representation(instance)

    def update(self, instance, validated_data):
        data = self.context['request'].data
        print("update")
        try:
            family = Family.objects.get(family_ko=data.get('family.family_ko'), family_en=data.get('family.family_en'))
            genus = Genus.objects.get(genus_ko=data.get('genus.genus_ko'), genus_en=data.get('genus.genus_en'))
            instance.family = family
            instance.genus = genus
            instance.save()
        except Family.DoesNotExist or Genus.DoesNotExist:
            print("No family or No genus")

        return instance

    def post(self, request, format=None):
        print("포스트 요청")

