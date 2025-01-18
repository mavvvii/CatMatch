from rest_framework import serializers

from cats.models.shelter import Shelter
from cats.models.cat import Cat
from cats.models.cats_adopted import CatAdopted
from cats.models.cat_photos import CatPhotos
from user.models import User


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


class CatAdoptedDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatAdopted
        fields = '__all__'
