from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.request import Request


from cats.models import CatPhotos, Cat
from cats.serializers import CatPhotosListSerializer, CatPhotosDetailSerializer

from uuid import UUID
from typing import List, Type
import os
from django.conf import settings


class CatPhotosViewSet(viewsets.ModelViewSet):
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    lookup_field: str = 'cat'
    lookup_url_kwarg: str = 'cat_id'

    def get_serializer_class(self) -> Type[CatPhotosDetailSerializer | CatPhotosListSerializer]:
        if self.action in ['list', 'retrieve']:
            return CatPhotosListSerializer
        return CatPhotosDetailSerializer

    def get_queryset(self) -> QuerySet:
        return CatPhotos.objects.all()

    def list(self, request: Request) -> Response:
        """GET /api/catmatch/cats-photos/ - Pobiera wszystkie zdjęcia kotów"""
        photos = self.get_queryset()
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """GET /api/catmatch/cats-photos/{cat_id}/ - Pobiera wszystkie zdjęcia dla konkretnego kota"""
        cat_id = kwargs.get('cat_id')
        photos = self.get_queryset().filter(cat=str(cat_id))
        if not photos.exists():
            return Response({'detail': 'No photos found for this cat'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        """POST /api/catmatch/cats-photos/ - Dodaje zdjęcie dla kota"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            cat_id = serializer.validated_data.get('cat').id
            if not Cat.objects.filter(id=cat_id).exists():
                return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)
            photo = serializer.save()
            return Response(self.get_serializer(photo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

