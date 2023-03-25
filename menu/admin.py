from django.contrib import admin

from menu.models import Menu
from menu.models import MenuItem


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_is_named', 'url', 'parent', 'order')
    list_filter = ('title',)
    search_fields = ('title', 'url')


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)