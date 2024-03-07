from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe

import locale
import os

locale.setlocale(locale.LC_ALL, "")
register = template.Library()


@register.inclusion_tag("auctions/components/input-group.html")
def custom_input(name, type, placeholder, label):
    return {"name": name, "type": type, "placeholder": placeholder, "label": label}


@register.inclusion_tag("auctions/components/optional-input-group.html")
def custom_optional_input(name, type, placeholder, label):
    return {"name": name, "type": type, "placeholder": placeholder, "label": label}


@register.inclusion_tag("auctions/components/error-input-group.html")
def custom_error_input(name, type, placeholder, label):
    return {"name": name, "type": type, "placeholder": placeholder, "label": label}


@register.inclusion_tag("auctions/components/submit-button.html")
def custom_submit_button(text):
    return {
        "text": text,
    }


@register.simple_tag
def svg_icon(file_name):
    print(settings.BASE_DIR)
    svg_path = os.path.join(
        settings.BASE_DIR, "auctions/static/icons", file_name + ".svg"
    )
    print(svg_path)
    with open(svg_path, "r") as file:
        svg_code = file.read()

    svg_code = format_html(svg_code)
    return mark_safe(svg_code)

@register.filter()
def currency(value):
    return locale.currency(value, grouping=True)
