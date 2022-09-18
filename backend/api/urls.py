from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewSet,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingCartViewSet,
    SignUp,
    FollowViewSet,
    TagViewSet,
    Token,
    UserViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet)
router.register(
    r"recipes/(?P<recipes_id>\d+)/shopping_cart",
    ShoppingCartViewSet,
    basename="shopping_cart",
)
router.register(
    r"recipes/(?P<recipes_id>\d+)/favorite",
    FavoriteViewSet,
    basename="favorite",
)
router.register(
    r"users/(?P<users_id>\d+)/subscribe",
    FollowViewSet,
    basename="subscribe",
)
router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path("/auth/signup/", SignUp.as_view(), name="signup"),
    path("/auth/token/", Token.as_view(), name="token"),
    path("/", include(router.urls)),
]
