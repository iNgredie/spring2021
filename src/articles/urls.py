from src.users.utils import OptionalSlashRouter
from .views import ArticleViewSet


router = OptionalSlashRouter()
router.register(r'article/?', ArticleViewSet)
urlpatterns = router.urls
