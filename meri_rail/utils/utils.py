"""Utilities Functions for PNR Scrapping"""

from rest_framework_simplejwt.tokens import RefreshToken
import json


def load_data(filepath: str) -> dict:
    """
    Load data from json file.
    :param filepath: str
    :return: dict
    """
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def get_model(app_label, model_name):
    """Returns Model Instance"""
    from django.apps import apps

    return apps.get_model(app_label=app_label, model_name=model_name)


class AuthService:
    def __tokens_for_user(self, user) -> dict:
        """generate tokens"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_auth_tokens_for_user(self, user) -> dict:
        """call private method to generate refresh and access token"""
        return self.__tokens_for_user(user)
