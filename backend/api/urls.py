from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from .views import (
    FavouriteViewSet,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingCartViewSet,
    FollowViewSet,
    TagViewSet,
    CustomUserViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("users", CustomUserViewSet)
router.register(
    r"users/(?P<users_id>\d+)/subscribe",
    FollowViewSet,
    basename="subscribe",
)
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<recipes_id>\d+)/favourite",
    FavouriteViewSet,
    basename="favourite",
)
router.register(
    r"recipes/(?P<recipes_id>\d+)/shopping_cart",
    ShoppingCartViewSet,
    basename="shopping_cart",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
