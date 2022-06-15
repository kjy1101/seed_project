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
        fields = ['url', 'id', 'intro_num', 'family', 'genus', 'used_scientific_name', 'plant_name', 'microscope', 'grain',
                  'seed_length', 'seed_length_error', 'seed_width', 'seed_width_error', 'note', 'images']

    def create(self, validated_data):
        instance, check = Seed.objects.get_or_create(
            intro_num=validated_data.get('intro_num'),
            family_id=validated_data.get('family').id,
            genus_id=validated_data.get('genus').id,
            used_scientific_name=validated_data.get('used_scientific_name'),
            plant_name=validated_data.get('plant_name'),
            microscope=validated_data.get('microscope'),
            seed_length=validated_data.get('seed_length'),
            seed_width=validated_data.get('seed_width'),
            seed_width_error=validated_data.get('seed_width_error'),
            seed_length_error=validated_data.get('seed_length_error'),
            note=validated_data.get('note'),
            grain=validated_data.get('grain')
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
        print("update")

        instance.intro_num=validated_data.get('intro_num')
        instance.family_id=validated_data.get('family').id
        instance.genus_id=validated_data.get('genus').id
        instance.used_scientific_name=validated_data.get('used_scientific_name')
        instance.plant_name=validated_data.get('plant_name')
        instance.microscope=validated_data.get('microscope')
        instance.seed_length=validated_data.get('seed_length')
        instance.seed_width=validated_data.get('seed_width')
        instance.seed_width_error=validated_data.get('seed_width_error')
        instance.seed_length_error=validated_data.get('seed_length_error')
        instance.note=validated_data.get('note')
        instance.grain=validated_data.get('grain')
        
        instance.save()

        return instance