from django.contrib import admin
from blog.models import Post,comments
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','status','body','publish','created','updated']
    prepopulated_fields={'slug':('title',)}
    list_filter=('status','author',)
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hirearchy='publish'
    ordering=['status','publish']

class commentsadmin(admin.ModelAdmin):
    list_display=['post','name','email','body','created','updated','active']
    list_filter=('created','name',)
    search_fields=('name','email')

admin.site.register(Post,PostAdmin)
admin.site.register(comments,commentsadmin)
