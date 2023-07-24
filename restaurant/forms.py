from django import forms
from django.utils import timezone


class BookingForm(forms.Form):
    name = forms.CharField(max_length=255)
    no_of_guests = forms.IntegerField(initial=6)
    booking_date = forms.DateField(initial=timezone.now().date())
