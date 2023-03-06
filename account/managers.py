from django.contrib.auth.models import (
    BaseUserManager,
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(_("Superuser Account: You must provide an email address"))

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(_("Customer Account: You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user