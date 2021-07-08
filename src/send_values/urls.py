from src.users.utils import OptionalSlashRouter

from .views import (
    WaterGasElectricalMetersViewSet,
    ValuesViewSet,
    MetersTypeViewSet,
)

app_name = 'send_values'


urlpatterns = []

router = OptionalSlashRouter()

router.register(r'meter/?', WaterGasElectricalMetersViewSet, basename='meter')
router.register(r'values/?', ValuesViewSet, basename='values')
router.register(r'metertypes/?', MetersTypeViewSet, basename='metertypes')

urlpatterns += router.urls
