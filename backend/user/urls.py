from user.views.user_view import UserReadOnlyViewSet
from user.views.auth_view import UserRegistrationView, UserLoginView, UserUpdateView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'', UserReadOnlyViewSet, basename='users')
router.register(r'update', UserUpdateView, basename='user-update')
router.register(r'auth/register', UserRegistrationView, basename='auth-register')
router.register(r'auth/login', UserLoginView, basename='auth-login')

urlpatterns = router.urls