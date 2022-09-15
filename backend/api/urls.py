from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUp,
    TitleViewSet,
    Token,
    UserViewSet,
)

app_name = "api"

router = DefaultRouter()
# router.register("categories", CategoryViewSet)
# router.register("genres", GenreViewSet)
# router.register("titles", TitleViewSet)
# router.register(
#     r"titles/(?P<title_id>\d+)/reviews",
#     ReviewViewSet,
#     basename="review",
# )
# router.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet,
#     basename="comment",
# )
router.register("users", UserViewSet)

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view(), name="signup"),
    path("v1/auth/token/", Token.as_view(), name="token"),
    path("v1/", include(router.urls)),
]
