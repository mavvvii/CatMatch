from rest_framework.routers import DefaultRouter
from cats.views.cat_view import CatViewSet
from cats.views.cat_adopted_view import CatAdoptedViewSet
from cats.views.shelter_view import ShelterViewSet
from cats.views.cat_photos_view import CatPhotosViewSet

# from django.conf.urls.static import static
# from django.conf import settings

router = DefaultRouter()

router.register(r'cats', CatViewSet, basename='cats')
router.register(r'cats-adopted', CatAdoptedViewSet, basename='cats-adopted')
router.register(r'shelters', ShelterViewSet, basename='shelters')
router.register(r'cats-photos', CatPhotosViewSet, basename='cats-photos')

urlpatterns = router.urls
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)