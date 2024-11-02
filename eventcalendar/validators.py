
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class NumericPasswordValidator:
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("Your password can’t be entirely numeric.")
    
    
class SpecialCharacterPasswordValidator:
    """
    Validate that the password contains at least one special character.
    """

    def validate(self, password, user=None):
        if not re.search(r'[.,?\"\'\-#]', password):
            raise ValidationError(
                _("This password must contain at least one special character (.,?\"'-#)."),
                code="password_no_special_character",
            )

    def get_help_text(self):
        return _("Your password must contain at least one special character: .,?\"'-#.")


class LowercasePasswordValidator:
    """
    Validate that the password contains at least one lowercase letter.
    """

    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("This password must contain at least one lowercase letter."),
                code="password_no_lowercase",
            )

    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter (a-z).")
    
class UppercasePasswordValidator:
    """
    Validate that the password contains at least one uppercase letter.
    """

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code="password_no_uppercase",
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter (A-Z).")


class NumericCharacterPasswordValidator:
    """
    Validate that the password contains at least one numeric character.
    """

    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                _("This password must contain at least one numeric character."),
                code="password_no_numeric",
            )

    def get_help_text(self):
        return _("Your password must contain at least one numeric character (0-9).")