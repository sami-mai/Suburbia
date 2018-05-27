from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from .forms import LookupForm
from burbnews.models import Topic
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.template import RequestContext


class LookupView(FormView):
    form_class = LookupForm

    def get(self, request):
        return render_to_response('suburb/lookup.html', RequestContext(request))

    def form_valid(self, form):
        # Get data
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        # Get today's date
        now = timezone.now()

        # Get next week's date
        next_week = now + timezone.timedelta(weeks=1)

        # Get Point
        location = Point(longitude, latitude, srid=4326)

        # Look up topics
        topics = Topic.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('suburb__location', location)).order_by('distance')[0:5]

        # Render the template
        return render_to_response('suburb/lookupresults.html', {
            'topics': topics
            })