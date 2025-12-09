from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/<int:audit_id>/', views.report, name='report'),
    path('download/<int:audit_id>/', views.download_pdf, name='download_pdf'),
]
