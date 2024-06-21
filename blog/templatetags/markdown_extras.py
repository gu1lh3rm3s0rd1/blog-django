import markdown
from django import template
from django.utils.safestring import mark_safe
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    extensions = [CodeHiliteExtension(linenums=False), 'fenced_code', 'tables']
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)
