from src.users.utils import OptionalSlashRouter
from .views import TaskViewSet, TaskStatusViewSet


router = OptionalSlashRouter()
router.register(r'task/?', TaskViewSet)
router.register(r'task_status/?', TaskStatusViewSet)
urlpatterns = router.urls
