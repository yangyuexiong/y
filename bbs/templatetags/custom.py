
from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def truncate_url(img_obj):

    return img_obj.name.split("/",maxsplit=1)[-1]
