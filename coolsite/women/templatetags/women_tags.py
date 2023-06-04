from django import template
from women.models import *

register = template.Library() # так регистрируем свио теги

@register.simple_tag(name='getcats')# по этому имени тег будет доступен после импорта
def get_categories(filter=None): #возвращаем коллекцию данных
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)



@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0): #возвращаем фрагмент html
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}

