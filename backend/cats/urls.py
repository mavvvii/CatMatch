from rest_framework.routers import DefaultRouter
from cats.views.cat_view import CatViewSet
from cats.views.cat_adopted_view import CatAdoptedViewSet
from cats.views.shelter_view import ShelterViewSet

router = DefaultRouter()

router.register('cat', CatViewSet, basename='cat')
router.register('cats/adopted', CatAdoptedViewSet, basename='cats_adopted')
router.register('shelter', ShelterViewSet, basename='shelter')

urlpatterns = router.urls