from django.contrib import admin
from blog.models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Display labels
    list_display =['title','slug','author','publish','status']
    # Filters
    list_filter = ['status','created','publish','author']
    # Search and filter by 'title' and 'body'
    search_fields= ['title','body']
    # Slug auto generating by title 
    prepopulated_fields={'slug':('title',)}
    # Searching by id number
    raw_id_fields=['author']
    # Filtering by a publishing date
    date_hierarchy='publish'
    # Ordering by "status" or "publish"
    ordering= ['status','publish']
