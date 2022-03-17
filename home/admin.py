from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.AppUser)
admin.site.register(models.InstagramPage)
admin.site.register(models.ResourceFile)
admin.site.register(models.MediaFile)


@admin.register(models.Post)
class PostAmin(admin.ModelAdmin):
    def __init__(self, model, admin_site) -> None:
        self.list_display = ['post_id', 'user_name', 'caption_text']
        self.list_select_related = ['user', 'resource']
        self.change_list_template = 'action.html'
        self.list_per_page= 50
        self.list_filter = ['user']
    
        super().__init__(model, admin_site)
    
    def user_name(self, post):
        return post.user.username
    