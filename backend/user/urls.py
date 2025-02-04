from user.views import UserViewSet, UserRegistrationView, UserLoginView, UserUpdateView, AddToShelterStaffView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', UserViewSet, basename='users')
router.register(r'update', UserUpdateView, basename='user-update')
router.register(r'auth/register', UserRegistrationView, basename='auth-register')
router.register(r'auth/login', UserLoginView, basename='auth-login')
router.register(r'group', AddToShelterStaffView, basename='group')

urlpatterns = router.urls