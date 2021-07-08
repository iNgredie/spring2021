from src.users.utils import OptionalSlashRouter

from src.services.views import ServiceView, PriceListView

urlpatterns = []

router = OptionalSlashRouter()
router.register(r'service/?', ServiceView)
router.register(r'price/?', PriceListView)

urlpatterns += router.urls
