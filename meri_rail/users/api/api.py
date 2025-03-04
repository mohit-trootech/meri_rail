import os
from rest_framework import permissions, status
from rest_framework.response import Response
from utils.utils import get_model
from users.api.serializers import (
    UserSerializer,
    UserSerializerBase,
    GoogleAuthenticationLogin,
    GoogleAuthenticationSignup,
)
from utils.auth_service import AuthService
from users.constants import ResponseMessages, AUTHENTICATED_USER_CACHE_KEY
from utils.constants import AppLabelsModel, CacheTimeout
from rest_framework.decorators import action
from django.shortcuts import redirect
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from django.core.cache import cache

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
User = get_model(**AppLabelsModel.USERS)
GoogleOAuth2Token = get_model(**AppLabelsModel.GOOGLE_OAUTH2_TOKEN)
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


class UserProfileView(RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        """Return User Profile"""
        instance = self.get_object()
        cached_data = cache.get(AUTHENTICATED_USER_CACHE_KEY % instance.email)
        if cached_data:
            return Response(
                cached_data,
                status=status.HTTP_200_OK,
            )
        serializer = UserSerializerBase(instance, context={"request": request})
        cache.set(
            AUTHENTICATED_USER_CACHE_KEY % instance.email,
            serializer.data,
            timeout=CacheTimeout.ONE_DAY,
        )
        return Response(serializer.data)

    def get_object(self, *args, **kwargs):
        """Return User Object"""
        return self.request.user


class GoogleAuthServiceView(GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthenticationSignup
    login_serializer_class = GoogleAuthenticationLogin

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        """Google Login"""
        serializer = self.login_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(google_id=serializer.data["google_id"])
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=serializer.data["email"])
            except User.DoesNotExist:
                return Response(
                    {"message": ResponseMessages.USER_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            AuthService().get_auth_tokens_for_user(user),
            status=status.HTTP_200_OK,
        )

    def get_flow_from_client_config(self):
        return Flow.from_client_config(
            client_config=settings.CLIENT_CONFIG,
            scopes=SCOPES,
            redirect_uri=settings.REDIRECT_URI,
        )

    @action(methods=["GET"], detail=False)
    def init(self, request):
        if not settings.REDIRECT_URI:
            return Response(
                {
                    "message": "message"
                    "Redirect Url or Web Client Config is not configured"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        flow = self.get_flow_from_client_config()
        if not flow:
            return Response(
                {"message": "Google Auth Init Failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        auth_url, state = flow.authorization_url()
        return redirect(auth_url)

    @action(methods=["GET"], detail=False)
    def callback(self, request):
        try:
            if not settings.REDIRECT_URI:
                return Response(
                    {
                        "message": "message"
                        "Redirect Url or Web Client Config is not configured"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            flow = self.get_flow_from_client_config()
            flow.fetch_token(authorization_response=request.build_absolute_uri())
            credentials = flow.credentials
            service = build("oauth2", "v2", credentials=credentials)
            user_info = service.userinfo().get().execute()
            user = GoogleAuthenticationSignup(
                data={
                    "google_id": user_info["id"],
                    "email": user_info["email"],
                    "username": user_info["email"],
                    "first_name": user_info["given_name"],
                    "last_name": user_info["family_name"],
                    "image": user_info.get("picture", None),
                }
            )
            user.is_valid(raise_exception=True)
            instance, created = user.save()
            GoogleOAuth2Token.objects.update_or_create(
                user=instance,
                defaults={
                    "access_token": credentials.token,
                    "refresh_token": credentials.refresh_token,
                    "expires_at": credentials.expiry,
                },
            )
            request.session["context"] = {
                "title": "Meri Rail",
                "content": "Welcome to Meri Rail, Please Close this Window and Continue Login.",
            }
            return redirect("/success/")
        except Exception as err:
            request.session["context"] = {
                "title": "Meri Rail Exception",
                "content": str(err),
            }
            return redirect("/error/")
