from django.contrib import admin
from django.urls import path
from scaler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('state/', views.state),
    path('scale/up/', views.scale_up),
    path('scale/down/', views.scale_down),
]
