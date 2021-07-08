from django.contrib import admin

from .models import (
    WaterGasElectricalMeters,
    ValueWaterGasElectricalMeters,
    MetersType
)

admin.site.register(WaterGasElectricalMeters)
admin.site.register(ValueWaterGasElectricalMeters)
admin.site.register(MetersType)
