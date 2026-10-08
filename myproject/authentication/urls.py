from django.urls import path
from .views import GoogleLoginView,TokenRefreshView,LogoutView

urlpatterns=[
    path('login/',GoogleLoginView.as_view(),name='google-login'),
    path('refresh/',TokenRefreshView.as_view(),name="token-refresh"),
    path('logout/',LogoutView.as_view(),name="logout")
]
