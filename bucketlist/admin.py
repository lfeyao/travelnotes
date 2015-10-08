from django.contrib import admin
from .models import Category, Page, Place


class PageAdmin(admin.ModelAdmin):
    #inlines = [PageInline]
    list_display = ('name', 'category', 'likes', 'was_done', 'date_added')
    list_filter = ['category']
    search_fields = ['name']

class PlaceAdmin(admin.ModelAdmin):
    #inlines = [PageInline]
    list_display = ('name', 'category', 'location', 'likes')
    list_filter = ['category']
    search_fields = ['name']

# Register your models here.

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(Place, PlaceAdmin)