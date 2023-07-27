
from django import template

register = template.Library()

@register.filter
def key(d, key_name):
    return d.get(key_name)
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from django import template

register = template.Library()

@register.filter
def day(queryset, day):
    return queryset.filter(date__day=day)
from django import template

register = template.Library()

@register.filter
def day(queryset, day):
    return queryset.filter(date__day=day)




from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


register = template.Library()

@register.filter(name='index')
def index_filter(value, arg):
    return value[arg]



from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
