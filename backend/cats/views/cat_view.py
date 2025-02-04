from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.request import Request

from cats.models import Cat, Shelter
from cats.serializers import CatListSerializer, CatDetailSerializer

from typing import List, Type
from uuid import UUID


class CatViewSet(viewsets.ModelViewSet):
    permission_classes: List[Type[BasePermission]] = [AllowAny]

    lookup_field: str = 'id'
    lookup_url_kwarg: str = 'id'

    def get_serializer_class(self) -> Type[CatListSerializer | CatDetailSerializer]:
        if self.action == 'list':
            return CatListSerializer
        return CatDetailSerializer

    def get_queryset(self) -> QuerySet[Cat]:
        return Cat.objects.all()

    def list(self, request: Request) -> Response:
        cat: QuerySet[Cat] = self.get_queryset()
        serializer: CatListSerializer = self.get_serializer(cat, many = True)

        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        cat_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat: Cat = queryset.get(id = cat_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatDetailSerializer = self.get_serializer(cat)

        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer: CatDetailSerializer = CatDetailSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        shelter_id: UUID = request.data.get('shelter')

        try:
            shelter: Shelter = Shelter.objects.get(id = shelter_id)
        except Shelter.DoesNotExist:
            return Response({'error': 'Shelter not found'}, status=status.HTTP_404_NOT_FOUND)

        cat: Cat = Cat.objects.create(
            name = serializer.validated_data['name'],
            age = serializer.validated_data['age'],
            breed = serializer.validated_data.get('breed'),
            gender = serializer.validated_data['gender'],
            color = serializer.validated_data.get('color'),
            notes = serializer.validated_data.get('notes'),
            shelter = shelter,
        )

        return Response(CatDetailSerializer(cat).data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        cat_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat: Cat = queryset.get(id = cat_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatDetailSerializer = self.get_serializer(cat, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        cat_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat: Cat = queryset.get(id = cat_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatDetailSerializer = self.get_serializer(cat, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        cat_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat: Cat = queryset.get(id=cat_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found'}, status=status.HTTP_404_NOT_FOUND)

        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)