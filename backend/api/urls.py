from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from .views import (
    FavouriteViewSet,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingCartViewSet,
    # SignUp,
    FollowViewSet,
    TagViewSet,
    UserViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("users", UserViewSet)
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
    # path("auth/signup/", SignUp.as_view(), name="signup"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
