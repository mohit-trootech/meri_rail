from rest_framework import permissions, views, status
from rest_framework.response import Response
from utils.utils import get_model
from users.api.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    EmailUpdateSerializer,
    EmailVerifySerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    GoogleAuthenticationLogin,
    GoogleAuthenticationSignup,
)
from utils.auth_service import AuthService
from rest_framework.generics import UpdateAPIView, CreateAPIView
from users.constants import ResponseMessages
from utils.constants import AppLabelsModel

User = get_model(**AppLabelsModel.USERS)

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


class RegistrationApiView(CreateAPIView):
    """User Registeration API View"""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class LoginApiView(views.APIView):
    """User Login API View"""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            AuthService().get_auth_tokens_for_user(serializer.validated_data),
            status=status.HTTP_200_OK,
        )


class UserProfileView(views.APIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        """Return User Object"""
        return self.request.user

    def get(self, *args, **kwargs):
        """Return User Profile"""
        instance = self.get_object(*args, **kwargs)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Update User Profile"""
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmailUpdateView(views.APIView):
    """User Email Update View"""

    serializer_class = EmailUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, *args, **kwargs):
        """Update User Email"""
        serializer = self.serializer_class(
            self.request.user, data=self.request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyView(UpdateAPIView):
    """Email Verification API View"""

    serializer_class = EmailVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Send Email Verification OTP"""
        try:
            return Response(
                {"message": ResponseMessages.OTP_GENERATED}, status=status.HTTP_200_OK
            )
        except Exception as err:
            raise Response(
                {
                    "message": ResponseMessages.FAILED_TO_GENERATE_OTP.format(err=err),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        """Verify User Email"""
        serializer = self.serializer_class(
            instance=request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": ResponseMessages.EMAIL_VERIFIED},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(UpdateAPIView):
    """Change Password API View"""

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """Change User Password"""
        serializer = self.serializer_class(
            instance=request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": ResponseMessages.PASSWORD_CHANGED_DONE},
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(UpdateAPIView):
    """Forgot Password API View"""

    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Forgot Password Send Password Reset OTP to User"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": ResponseMessages.PASSWORD_RESET_OTP_GENERATED},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """Update User Password After Verification"""
        user = User.objects.get(email=request.data["email"])
        serializer = self.serializer_class(
            instance=user, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": ResponseMessages.PASSWORD_RESET_DONE},
            status=status.HTTP_200_OK,
        )


class GoogleSignupView(CreateAPIView):
    """Google Signup API View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthenticationSignup

    def post(self, request, *args, **kwargs):
        """Create New User"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GoogleLoginView(CreateAPIView):
    """Google Login API View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthenticationLogin

    def post(self, request, *args, **kwargs):
        """Google Login"""
        serializer = self.serializer_class(data=request.data)
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


from django.shortcuts import redirect  # noqa
from django.contrib.auth import login, get_user_model  # noqa
from google.oauth2.credentials import Credentials  # noqa
from googleapiclient.discovery import build  # noqa
from google_auth_oauthlib.flow import Flow  # noqa
from django.conf import settings  # noqa
import datetime  # noqa
from users.models import GoogleOAuth2Token  # noqa
from django.views.decorators.csrf import csrf_exempt  # noqa
from django.http import JsonResponse  # noqa


@csrf_exempt
def google_auth_init(request):
    flow = Flow.from_client_config(
        client_config=settings.CLIENT_CONFIG_JSON,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/google/callback",
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent"
    )
    request.session["state"] = state
    return JsonResponse({"auth_url": authorization_url, "state": state})


import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@csrf_exempt
def google_auth_callback(request):
    state = request.session.pop("state", "")
    flow = Flow.from_client_config(
        client_config=settings.CLIENT_CONFIG_JSON,
        scopes=SCOPES,
        state=state,
        redirect_uri="http://localhost:8000/auth/google/callback",
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    User = get_user_model()

    # Get user info
    service = build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()

    # Create or update user
    user, created = User.objects.get_or_create(email=user_info["email"])
    if created:
        user.username = user_info["email"]
        user.save()
    GoogleOAuth2Token.objects.update_or_create(
        user=user,
        defaults={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_at": credentials.expiry,
        },
    )

    login(request, user)
    print(user)
    return redirect("http://localhost:3000/")
