from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from menu.models import Menu, MenuItem

register = template.Library()


def get_ancestor_titles(menu_item):
    ancestor_titles = []
    parent = menu_item.parent
    while parent is not None:
        ancestor_titles.append(parent.title)
        parent = parent.parent
    return '/'.join(ancestor_titles[::-1])


def is_path_matching_menu_item(menu_item, path):
    path = '/'.join(list(filter(lambda x: x != '', path.split('/'))))
    ancestor_titles = get_ancestor_titles(menu_item)

    if len(ancestor_titles) > 0:
        ancestor_titles += '/' + menu_item.title
    else:
        ancestor_titles += menu_item.title

    if ancestor_titles == path:
        return True
    else:
        return False


def is_menu_item_path_active(menu_item, path):
    try:
        if is_path_matching_menu_item(menu_item, path):
            return True

        for child in menu_item.children.all():
            if is_path_matching_menu_item(child, path):
                return True

        return False
    except NoReverseMatch:
        return False


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    try:
        request = context.get('request')
        menu_item_path = request.path

        menu_item_titles = menu_item_path.strip('/').split('/')
        active_item_title = menu_item_titles[-1]
        active_items = MenuItem.objects.filter(title=active_item_title)

        if len(active_item_title) > 0:
            active_item = active_items.first()
            if active_items.exists() and is_path_matching_menu_item(active_item, menu_item_path):
                menu = Menu.objects.prefetch_related('menuitem_set__children').get(name=menu_name)
                return render_menu(menu.menuitem_set.filter(parent=None), menu_item_path)
            else:
                return ''
        else:
            menu = Menu.objects.prefetch_related('menuitem_set__children').get(name=menu_name)
            return render_menu(menu.menuitem_set.filter(parent=None), menu_item_path)
    except (ObjectDoesNotExist, NoReverseMatch) as e:
        return ''


def render_menu(menu_items, path):
    if not menu_items:
        return ''
    html = '<ul>'

    for menu_item in menu_items.order_by('order'):
        active = is_menu_item_path_active(menu_item, path)

        if menu_item.url_is_named:
            url = reverse(menu_item.url)
        else:
            url = menu_item.url

        html += '<li class="active">' if active else '<li>'
        html += '<a href="{}">{}</a>'.format(url, menu_item.title)

        children = MenuItem.objects.filter(parent=menu_item.id)
        if menu_items.exists() and (active or any(is_menu_item_path_active(child, path) for child in children)):
            html += render_menu(children, path)

        html += '</li>'
    html += '</ul>'

    return mark_safe(html)
