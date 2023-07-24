from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.views import View

from .forms import BookingForm

import requests, json

import environ

env = environ.Env()
environ.Env.read_env()


def get_token():
    url = 'http://127.0.0.1:8000/api/token/login/'
    data = {
        'username': env('USERNAME'),
        'password': env('PASSWORD')
    }
    response = requests.post(url, data=data)
    response_dict = json.loads(response.text)
    return response_dict.get('access')

def get_auth_header():
    token =get_token()
    return {'Authorization': f'JWT {token}'}


def index(request):
    return render(request, 'restaurant/index.html', {})


def about(request):
    return render(request, 'restaurant/about.html')


def menu(request):
    url = f"http://127.0.0.1:8000{reverse('api:menu')}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    return render(request, 'restaurant/menu.html', context={'menu_items': json.loads(response.text)})


def menu_item(request, pk):
    url = f"http://127.0.0.1:8000{reverse('api:menu-detail', kwargs={'pk': pk})}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    return render(request, 'restaurant/menu_item.html', context={'menu_item': json.loads(response.text)})


class Book(View):
    form_class = BookingForm
    template_name = 'restaurant/book.html'

    def get(self, request):
        token = get_token()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'token': token})

    def get_data_from_form(self, form):
        data = {
            'name': form.cleaned_data.get('name'),
            'no_of_guests': form.cleaned_data.get('no_of_guests'),
            'booking_date': form.cleaned_data.get('booking_date'),
        }
        return data

    def post(self, request):
        token = get_token()
        form = self.form_class(request.POST)
        if form.is_valid():
            data = self.get_data_from_form(form)
            headers = get_auth_header()
            url = f"http://127.0.0.1:8000{reverse('api:bookings')}"
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 201:
                context = {'form': BookingForm(), 'token': token}
                return render(request, 'restaurant/book.html', context)
        context = {'form': form, 'token': token}
        return render(request, 'restaurant/book.html', )


def bookings(request):
    if request.GET.get('date') is None:
        date = timezone.now().date()
    else:
        date = request.GET.get('date')
    url = f"http://127.0.0.1:8000{reverse('api:bookings')}?date={date}"
    headers = get_auth_header()
    response = requests.get(url, headers=headers)
    return render(request, 'restaurant/bookings.html', context={'bookings': response.text})
