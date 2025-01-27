from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from userapp.api.views import Registration_view, Logout

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', Registration_view, name = 'register'),
    path('logout/', Logout, name = 'logout'),
]
