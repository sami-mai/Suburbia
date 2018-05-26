from django.test import TestCase
from .models import Suburb
from factory.fuzzy import BaseFuzzyAttribute
from django.contrib.gis.geos import Point
import factory.django
import random
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from .views import LookupView


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0),
                     random.uniform(-90.0, 90.0))


# Factories for tests
class SuburbFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Suburb
        django_get_or_create = (
            'name',
            'location'
        )

    name = 'Wembley Arena'
    location = FuzzyPoint()


class SuburbTest(TestCase):
    def test_create_Suburb(self):
        # Create the Suburb
        Suburb = SuburbFactory()

        # Check we can find it
        all_Suburbs = Suburb.objects.all()
        self.assertEqual(len(all_Suburbs), 1)
        only_Suburb = all_Suburbs[0]
        self.assertEqual(only_Suburb, Suburb)

        # Check attributes
        self.assertEqual(only_Suburb.name, 'Wembley Arena')

        # Check string representation
        self.assertEqual(only_Suburb.__str__(), 'Wembley Arena')


class LookupViewTest(TestCase):
    """
    Test lookup view
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('lookup'))
        response = LookupView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('suburb/lookup.html')

    def test_post(self):
        # Create Suburbs to return
        v1 = SuburbFactory(name='Suburb1')
        v2 = SuburbFactory(name='Suburb2')
        v3 = SuburbFactory(name='Suburb3')
        v4 = SuburbFactory(name='Suburb4')
        v5 = SuburbFactory(name='Suburb5')
        v6 = SuburbFactory(name='Suburb6')
        v7 = SuburbFactory(name='Suburb7')
        v8 = SuburbFactory(name='Suburb8')
        v9 = SuburbFactory(name='Suburb9')
        v10 = SuburbFactory(name='Suburb10')


        # Set parameters
        lat = 52.3749159
        lon = 1.1067473

        # Put together request
        data = {
            'latitude': lat,
            'longitude': lon
        }
        request = self.factory.post(reverse('lookup'), data)
        response = LookupView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('suburb/lookupresults.html')
