from django import template
from djantimat.helpers import PymorphyProc

# https://pythondigest.ru/view/2067/ откуда узнал про djantimat

register = template.Library()


@register.filter(name='censor')
def censor(value):
    without_slang = PymorphyProc.replace(u'Здесь есть маты', repl='')
    return without_slang
