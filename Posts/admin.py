from django.contrib import admin
from .models import Post,Comment,Like
# Posts

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
