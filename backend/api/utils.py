import base64

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers


class Hex2NameColor(serializers.Field):
    """Hex-color в читабельный вид"""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("Для этого цвета нет имени")


class Base64ImageField(serializers.ImageField):
    """Декодер картринки из формата Base64"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


# def RecipeExtraActions(self, request, model):
#     if request.method == 'POST':
#         user = self.request.user
#         recipe = get_object_or_404(Recipe, id=pk)
#         data = {
#             "user": user.id,
#             "favorite": recipe.id,
#         }
#         serializer = FavoriteSerializer(
#             data=data, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     if request.method == 'DELETE':
#         user = request.user
#         recipe = get_object_or_404(Recipe, id=pk)
#         favorite = get_object_or_404(Favorite, user=user, favorite=recipe)
#         favorite.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
