from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.request import Request

from cats.models import Shelter
from cats.serializers import ShelterListSerializer, ShelterDetailSerializer

from typing import List, Type
from uuid import UUID


class ShelterViewSet(viewsets.ModelViewSet):
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    lookup_field: str = 'id'
    lookup_url_kwarg: str = 'id'

    def get_serializer_class(self) -> Type[ShelterListSerializer | ShelterDetailSerializer]:
        if self.action == 'list':
            return ShelterListSerializer
        return ShelterDetailSerializer

    def get_queryset(self) -> QuerySet[Shelter]:
        return Shelter.objects.all()

    def list(self, request: Request) -> Response:
        shelters: QuerySet[Shelter] = Shelter.objects.all()
        serializer: ShelterListSerializer = self.get_serializer(shelters, many=True)

        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs):
        shelter_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Shelter] = self.get_queryset()

        try:
            shelter: Shelter = queryset.get(id = shelter_id)
        except Shelter.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: ShelterDetailSerializer = self.get_serializer(shelter)

        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer: ShelterDetailSerializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(ShelterDetailSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        shelter_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Shelter] = self.get_queryset()

        try:
            shelter: Shelter = queryset.get(id = shelter_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: ShelterDetailSerializer = self.get_serializer(shelter, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args, **kwargs):
        shelter_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Shelter] = self.get_queryset()

        try:
            shelter: Shelter = queryset.get(id = shelter_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: ShelterDetailSerializer = self.get_serializer(shelter, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs):
        shelter_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Shelter] = self.get_queryset()

        try:
            shelter: Shelter = queryset.get(id = shelter_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        shelter.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)