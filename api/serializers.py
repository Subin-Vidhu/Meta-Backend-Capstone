from rest_framework import serializers

from restaurant.models import Menu, Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['name', 'no_of_guests', 'booking_date']


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'inventory']
        read_only = ['id']