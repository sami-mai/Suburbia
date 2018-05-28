from django.shortcuts import render_to_response, render, redirect
from django.views.generic.edit import FormView
from burbnews.models import Topic
from .forms import EditSuburbForm, EditUserForm, EditProfile
from .models import Resident, Suburb
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
import requests
from decouple import config


GOOGLE_MAP_API_KEY = config('GOOGLE_MAP_API_KEY')
IPSTACK_API_KEY = config('IPSTACK_API_KEY')


class LookupView(FormView, LoginRequiredMixin):
    form_class = EditSuburbForm

    def get(self, request):
        form_class = EditSuburbForm
        return render_to_response('suburb/_lookup.html', {"form_class": form_class})

    def form_valid(self, form):
        # Get data
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        # Get today's date
        now = timezone.now()

        # Get next week's date
        next_week = now + timezone.timedelta(weeks=1)

        # Get Point
        location = Point(longitude, latitude, srid=4326)

        # Look up topics
        topics = Topic.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('suburb__location', location)).order_by('distance')[0:5]

        # Render the template
        return render_to_response('burbnews/topic_list.html', {
            'topics': topics
            })


@login_required(login_url='/accounts/login/')
@transaction.atomic
def edit_profile(request, id):
    suburb_form = EditSuburbForm()
    current_user = request.user
    resident = Resident.objects.get(user=current_user.id)
    suburb_name = request.POST.get('suburb_name')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    suburb = Suburb(suburb_name=suburb_name, longitude=longitude, latitude=latitude)
    suburb.save()
    if request.method == 'POST':
        resident_form = EditProfile(request.POST, request.FILES, instance=current_user.resident)
        user_form = EditUserForm(request.POST, instance=current_user)
        if resident_form.is_valid() and user_form.is_valid():
            resident = resident_form.save(commit=False)
            user = user_form.save(commit=False)
            resident.user = current_user
            resident.save()
            user.save()

            return redirect('landing')
    else:
        resident_form = EditProfile()
        user_form = EditUserForm()
    context = {
        "current_user": current_user,
        "resident_form": resident_form,
        "user_form": user_form,
        "suburb_form": suburb_form,
        "resident": resident,
        }
    return render(request, 'suburb/residents_form.html', context)


def home(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get(f'http://freegeoip.net/json/{ip_address}?access_key={IPSTACK_API_KEY}')
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']

    context = {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': GOOGLE_MAP_API_KEY
        }

    return render(request, 'index.html', context)
