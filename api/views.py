from django.utils import timezone

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Menu, Booking
from .serializers import BookingSerializer, MenuSerializer


class MenuItemView(ListCreateAPIView):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class BookingView(ListCreateAPIView):
    model = Booking
    queryset = model.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.GET.get('date') is not None:
            date = request.query_params.get('date')
        else:
            date = timezone.now().date()
        self.queryset = self.queryset.filter(booking_date=date)
        return super().get(request)


class SingleBookingView(RetrieveUpdateDestroyAPIView):
    model = Booking
    queryset = model.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]