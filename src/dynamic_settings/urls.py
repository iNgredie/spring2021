from src.users.utils import OptionalSlashRouter
from .views import DynamicSettingsViewSet


router = OptionalSlashRouter()
router.register(r'settings/?', DynamicSettingsViewSet)
urlpatterns = router.urls
