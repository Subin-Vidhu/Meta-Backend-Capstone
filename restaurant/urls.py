from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name="about"),
    path('menu/', views.menu, name='menu'),
    path('menu-item/<int:pk>/', views.menu_item, name='menu-detail'),
    path('book/', views.Book.as_view(), name='book'),
    path('bookings/', views.bookings, name='bookings'),
]
