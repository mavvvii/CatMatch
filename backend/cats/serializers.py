from rest_framework import serializers

from cats.models.shelter import Shelter
from cats.models.cat import Cat
from cats.models.cats_adopted import CatAdopted
from cats.models.cat_photos import CatPhotos


class CatListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ['id', 'name']
        read_only_fields = ['shelter']


class CatDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = '__all__'


class ShelterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shelter
        fields = ['id', 'name']


class ShelterDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shelter
        fields = '__all__'

    def create(self, validated_data):
        return Shelter.objects.create(**validated_data)

class CatAdoptedListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatAdopted
        fields = ['id', 'cat', 'user']

class CatAdoptedDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatAdopted
        fields = '__all__'


class CatPhotosListSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all())

    class Meta:
        model = CatPhotos
        fields = ['id', 'photo', 'cat']


class CatPhotosDetailSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all())

    class Meta:
        model = CatPhotos
        fields = '__all__'