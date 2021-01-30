import re
from django.forms import Form
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

regex_hexadecimal = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


def is_valid_hexadecimal(value):
    is_hexadecimal = re.search(regex_hexadecimal, value)
    if not is_hexadecimal:
        raise ValidationError(
            _('%(value)s is not a hexadecimal color'),
            params={'value': value},
        )
    return True


def is_valid_background_color(value):
    try:
        is_valid_hexadecimal(value)
    except ValidationError:
        if not value.startswith('radial-gradient(') and not value.startswith('linear-gradient('):
            raise ValidationError(
                _('%(value)s is not a valid css property'),
                params={'value': value},
            )


class HexFormField(forms.CharField):
    default_validators = [is_valid_hexadecimal]


class BackgroundColorFormField(forms.CharField):
    default_validators = [is_valid_background_color]
    max_length = 200


# Snoweb SVG

class ThemeLightForm(Form):
    theme_light_primary = HexFormField(
        required=False,
        label=_('Color theme light primary'),
        help_text=_('Hexadecimal color')
    )
    theme_light_secondary = HexFormField(
        required=False,
        label=_('Color theme light secondary'),
        help_text=_('Hexadecimal color')
    )
    theme_light_tertiary = HexFormField(
        required=False,
        label=_('Color theme light tertiary'),
        help_text=_('Hexadecimal color')
    )


class ThemeDarkForm(Form):
    theme_dark_primary = HexFormField(
        required=False,
        label=_('Color theme dark primary'),
        help_text=_('Hexadecimal color')
    )
    theme_dark_secondary = HexFormField(
        required=False,
        label=_('Color theme dark secondary'),
        help_text=_('Hexadecimal color')
    )
    theme_dark_tertiary = HexFormField(
        required=False,
        label=_('Color theme dark tertiary'),
        help_text=_('Hexadecimal color')
    )


# App

class ThemeLightAppForm(Form):
    theme_light_background_body = BackgroundColorFormField(
        required=False,
        label=_('Color theme light background body'),
        help_text=_('Hexadecimal color, linear-gradient, radial-gradient')
    )


class ThemeDarkAppForm(Form):
    theme_dark_background_body = BackgroundColorFormField(
        required=False,
        label=_('Color theme dark background body'),
        help_text=_('Hexadecimal color, linear-gradient, radial-gradient')
    )
