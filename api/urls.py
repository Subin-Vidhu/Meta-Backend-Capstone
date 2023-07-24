from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('menu-items', views.MenuItemView.as_view(), name='menu'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menu-detail'),
    path('bookings', views.BookingView.as_view(), name='bookings'),
    path('bookings/<int:pk>', views.SingleBookingView.as_view(), name='booking-detail'),
]