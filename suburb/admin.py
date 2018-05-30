from django.contrib import admin
from . import models
from django.forms import ModelForm
from floppyforms.gis import PointWidget, BaseGMapWidget


class CustomPointWidget(PointWidget, BaseGMapWidget):
    class Media:
        js = ('/staticfiles/floppyforms/js/MapWidget.js',)


class SuburbAdminForm(ModelForm):
    class Meta:
        model = models.Suburb
        fields = ['suburb_name', 'latitude', 'longitude']
        widgets = {
            'location': CustomPointWidget()
        }


class SuburbAdmin(admin.ModelAdmin):
    form = SuburbAdminForm


admin.site.register(models.Suburb, SuburbAdmin)
admin.site.register(models.Resident)
