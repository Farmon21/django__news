from django.contrib import admin
from .models import News, Category, Contact, Comment


# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ['title', 'slug', 'publish_time', 'status']
    search_fields = ['title', 'body']
    date_hierarchy = 'publish_time'
    list_filter = ['status', 'created_time', 'publish_time']
    ordering = ['status', '-publish_time']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'text']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Category)
