from django.urls import path,include
from . import views
from .views import login_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('processed -info/', views.processed_info_view, name='processed_info'),
    path('accounts/', include('django.contrib.auth.urls')),

]

