
from rest_framework import routers
from .views import ProcessViewSet

router = routers.SimpleRouter()
router.register(r'process', ProcessViewSet)
urlpatterns = router.urls
