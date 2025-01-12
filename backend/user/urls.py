from user.views import UserViewSet, UserRegistrationView, UserLoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'login', UserLoginView, basename='login')

urlpatterns = router.urls