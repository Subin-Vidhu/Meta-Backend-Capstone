from django.test import Client, TestCase
from django.urls import reverse
import json

from api.serializers import MenuSerializer, BookingSerializer
from restaurant.models import Menu, Booking
from config.tests.mixins import (
    UserMixin,
    BookingMixin, SingleBookingMixin,
    MenuItemMixin, SingleMenuItemMixin,
)


class SetUpMixin:

    def setUp(self):
        self.user = self.create_user(
            username = 'test@email.com',
            password = 'testpasswd',
        )
        self.token = self.get_token(
            username = 'test@email.com',
            password = 'testpasswd',
        )
        self.client = Client(HTTP_AUTHORIZATION=f'JWT {self.token}')


class BookingViewTest(SetUpMixin, UserMixin, BookingMixin, TestCase):

    def setUp(self):
        self.create_bookings()
        return super().setUp()

    def test_list(self):
        response = self.client.get(reverse('api:bookings'))
        serializer = BookingSerializer(Booking.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {'name': 'pete', 'no_of_guests': 4, 'booking_date': '2023-03-04'}
        response = self.client.post(reverse('api:bookings'), data=data)
        serializer = BookingSerializer(Booking.objects.get(name='pete'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)


class SingleBookingViewTest(SetUpMixin, UserMixin, SingleBookingMixin, TestCase):

    def setUp(self):
        self.create_booking()
        return super().setUp()

    def test_retrieve(self):
        response = self.client.get(reverse('api:booking-detail', kwargs={'pk': self.booking.pk}))
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        data = json.dumps({'no_of_guests': 6, 'booking_date': '2023-03-06'})
        response = self.client.patch(
            reverse('api:booking-detail', kwargs={'pk': self.booking.pk}),
            data = data,
            content_type = 'application/json',
        )
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update(self):
        data = json.dumps({'name': 'will', 'no_of_guests': 6, 'booking_date': '2023-03-06'})
        response = self.client.put(
            reverse('api:booking-detail', kwargs={'pk': self.booking.pk}),
            data = data,
            content_type = 'application/json',
        )
        serializer = BookingSerializer(Booking.objects.get(pk=self.booking.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(reverse('api:booking-detail', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(Booking.objects.filter(pk=self.booking.pk).exists(), False)


class MenuItemViewTest(SetUpMixin, UserMixin, MenuItemMixin, TestCase):

    def setUp(self):
        self.create_menu_items()
        super().setUp()

    def test_list(self):
        response = self.client.get(reverse('api:menu'))
        serializer = MenuSerializer(Menu.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        data = {'title': 'latte', 'price': 2.99, 'inventory': 5}
        response = self.client.post(reverse('api:menu'), data=data)
        serializer = MenuSerializer(Menu.objects.get(title='latte'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)


class SingleMenuItemViewTest(SetUpMixin, UserMixin, SingleMenuItemMixin, TestCase):

    def setUp(self):
        self.create_menu_item()
        return super().setUp()

    def test_retrieve(self):
        response = self.client.get(reverse('api:menu-detail', kwargs={'pk': self.menu_item.pk}))
        serializer = MenuSerializer(Menu.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        data = json.dumps({'price': 3.99, 'inventory': 3})
        response = self.client.patch(
            reverse('api:menu-detail', kwargs={'pk': self.menu_item.pk}),
            data = data,
            content_type = 'application/json',
        )
        serializer = MenuSerializer(Menu.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update(self):
        data = json.dumps({'title': 'Apple Juice', 'price': 3.85, 'inventory': 7})
        response = self.client.put(
            reverse('api:menu-detail', kwargs={'pk': self.menu_item.pk}),
            data = data,
            content_type = 'application/json',
        )
        serializer = MenuSerializer(Menu.objects.get(pk=self.menu_item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(reverse('api:menu-detail', kwargs={'pk': self.menu_item.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        self.assertEqual(Menu.objects.filter(pk=self.menu_item.pk).exists(), False)
