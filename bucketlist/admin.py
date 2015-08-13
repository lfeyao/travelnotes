from django.contrib import admin
from .models import Category, Page

"""
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

"""

class PageAdmin(admin.ModelAdmin):
    #inlines = [PageInline]
    list_display = ('title', 'category', 'url', 'was_done')
    list_filter = ['category']
    search_fields = ['title']


# Register your models here.

admin.site.register(Category)
admin.site.register(Page, PageAdmin)