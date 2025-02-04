from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.request import Request

from cats.models import Cat, CatAdopted
from user.models import User
from cats.serializers import CatAdoptedListSerializer, CatAdoptedDetailSerializer

from uuid import UUID
from datetime import datetime
from typing import List, Type


class CatAdoptedViewSet(viewsets.ModelViewSet):
    permission_classes: List[Type[BasePermission]] = [AllowAny]

    lookup_field: str = 'id'
    lookup_url_kwarg: str = 'id'

    def get_serializer_class(self) -> Type[CatAdoptedListSerializer | CatAdoptedDetailSerializer]:
        if self.action == 'list':
            return CatAdoptedListSerializer
        return CatAdoptedDetailSerializer

    def get_queryset(self) -> QuerySet[CatAdopted]:
        return CatAdopted.objects.all()

    def list(self, request: Request) -> Response:
        adopted_cats: QuerySet[CatAdopted] = self.get_queryset()
        serializer: CatAdoptedDetailSerializer = self.get_serializer(adopted_cats, many=True)

        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        cat_adopted_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat_adopted: CatAdopted = queryset.get(id=cat_adopted_id)
        except CatAdopted.DoesNotExist:
            return Response({'detail': 'Adopted cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatAdoptedDetailSerializer = self.get_serializer(cat_adopted)

        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs) -> Response:
        cat_id: UUID = request.data.get('cat')
        user_id: UUID = request.data.get('user')
        adoption_date: date = request.data.get('adoption_date')

        if adoption_date:
            try:
                adoption_date = datetime.strptime(adoption_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST
                )

        try:
            cat: Cat = Cat.objects.get(id=cat_id)
            user: User = User.objects.get(id=user_id)
        except Cat.DoesNotExist:
            return Response({'detail': 'Cat not found.'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if CatAdopted.objects.filter(cat=cat).exists():
            return Response(
                {'detail': 'This cat has already been adopted.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cat_adopted: CatAdopted = CatAdopted.objects.create(
            cat=cat,
            user=user,
            adoption_date=adoption_date or datetime.now().date()  # Jeśli adoption_date jest None, użyj dzisiejszej daty
        )

        serializer: CatAdoptedDetailSerializer = self.get_serializer(cat_adopted)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        cat_adopted_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat_adopted: CatAdopted = queryset.get(id=cat_adopted_id)
        except CatAdopted.DoesNotExist:
            return Response({'detail': 'Adopted cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatAdoptedDetailSerializer = self.get_serializer(cat_adopted, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        cat_adopted_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat_adopted: CatAdopted = queryset.get(id=cat_adopted_id)
        except CatAdopted.DoesNotExist:
            return Response({'detail': 'Adopted cat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: CatAdoptedDetailSerializer = self.get_serializer(cat_adopted, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs):
        cat_adopted_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[Cat] = self.get_queryset()

        try:
            cat_adopted: CatAdopted = queryset.get(id=cat_adopted_id)
        except CatAdopted.DoesNotExist:
            return Response({'detail': 'Adopted cat not found'}, status=status.HTTP_404_NOT_FOUND)

        cat_adopted.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
