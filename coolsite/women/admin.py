from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published','time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo','get_html_photo', 'is_published', 'time_create')
    readonly_fields = ('time_create', 'get_html_photo')# сначала прописываем здесь не ред. поля, потом прописываем их в fields
    save_on_top = True# чтобы панель при редактировании была и наверху

    def get_html_photo(self, object):#Чтобы в админке выводились фото, а не пути к ним
        # object будет ссылаться на модель Women
        if object.photo:
            print(object.photo.url)
            return mark_safe(f"<img src='{object.photo.url}' alt='error path' width={50}>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)# обязательно вторм должен стоять

admin.site.register(Category, CategoryAdmin)