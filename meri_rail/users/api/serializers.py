from rest_framework import serializers
from utils.utils import get_model
from django.core.files.base import ContentFile
from requests import get
from utils.constants import AppLabelsModel

GoogleOAuth2Token = get_model(**AppLabelsModel.GOOGLE_OAUTH2_TOKEN)
User = get_model(**AppLabelsModel.USERS)


class UserSerializerBase(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            if obj.image:
                return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    class Meta:
        model = User
        fields = ("id", "username", "email", "get_full_name", "image")


class UserSerializer(UserSerializerBase):
    class Meta(UserSerializerBase.Meta):
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "address",
            "google_id",
            "image",
            "last_login",
            "date_joined",
            "activity_status",
        )
        extra_kwargs = {
            "username": {"read_only": True},
            "email": {"read_only": True},
            "google_id": {"read_only": True},
        }


class GoogleAuthenticationLogin(serializers.Serializer):
    google_id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False)


class GoogleAuthenticationSignup(GoogleAuthenticationLogin):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    image = serializers.CharField(required=False)

    def validate_image(self, value):
        try:
            if value:
                image_byte = get(value)
                return ContentFile(content=image_byte.content, name="profile_image.jpg")
        except Exception as err:
            raise serializers.ValidationError(str(err))

    def create(self, validated_data):
        try:
            user = User.objects.get(google_id=validated_data["google_id"])
            return user, False
        except User.DoesNotExist:
            return User.objects.create(**validated_data), True
