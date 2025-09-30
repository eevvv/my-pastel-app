
#
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lang/<str:lang>/', views.home, name='change_language'),

    # Авторизация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Защищенная страница
    path('protected/', views.protected_view, name='protected'),
]

