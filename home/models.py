from pyexpat import model
from django.db import models


class AppUser(models.Model):
    username = models.TextField()
    password = models.TextField()
    email = models.EmailField()
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    avatar = models.TextField(null=True, blank=True)
    banner = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class InstagramPage(models.Model):
    address = models.TextField()
    username = models.TextField()
    last_post = models.TextField(null=True, blank=True)
    name = models.TextField()
    desc = models.TextField()
    avatar = models.TextField()

    def __str__(self):
        return self.username


class ResourceFile(models.Model):
    post_id = models.TextField()


class MediaFile(models.Model):
    MEDIA_TYPE = [
        ('1', 'IMAGE'),
        ('2', 'VIDEO'),
    ]

    media_type = models.CharField(default=MEDIA_TYPE[0], choices=MEDIA_TYPE, max_length=1)
    media_id = models.TextField()
    thumbnail_url = models.TextField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    resource = models.ForeignKey(ResourceFile, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.thumbnail_url


class Post(models.Model):
    MEDIA_TYPE = [
        ('1', 'IMAGE'),
        ('2', 'VIDEO'),
        ('3', 'RESOURCE'),
    ]

    post_id = models.TextField()
    item_id = models.TextField()
    media_type = models.CharField(default=MEDIA_TYPE[0], choices=MEDIA_TYPE, max_length=1)
    thumbnail_url = models.TextField(null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)
    user = models.ForeignKey(InstagramPage, on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    caption_text = models.TextField(null=True, blank=True)
    resource = models.ForeignKey(ResourceFile, on_delete=models.CASCADE, null=True, blank= True)

    def __str__(self):
        return self.post_id

    class Meta:
        db_table = ''
        ordering = ['-like_count']


class Review(models.Model):
    username = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
