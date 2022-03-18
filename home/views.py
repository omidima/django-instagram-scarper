from typing import List
import requests
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.conf import settings
from .models import  InstagramPage, ResourceFile, MediaFile, Post, Review
from .utils.instagram import Instagram
from .serializer import PostSerializer, MediaSerializer, ReviewSerializer
from instagrapi.types import Media, Resource
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import random
import os


class GetInstagramPosts(View):
    def get(self,req):
        users = InstagramPage.objects.all()
        
        for user in users:
            print('username: user: ',user.username)
            if user.last_post:
                posts = Instagram(username=user.username).getUserPosts(end_post=user.last_post)
                if len(posts[0]) > 0:
                    users.filter(pk= user.pk).update(last_post= posts[0][-1].pk)

            else:
                posts = Instagram(username=user.username).getUserPosts()
                endpost = posts[0][-1].pk
                users.filter(pk= user.pk).update(last_post= endpost)

            for post in posts[0]:
                print('username: posts: ', post.pk)
                if post.media_type == 8 :
                    m = self.create_media(post_id=post.pk, resources= post.resources)
                    p = Post(
                        post_id = post.pk,
                        item_id = post.id,
                        media_type = '3',
                        thumbnail_url = m[1][0].thumbnail_url,
                        video_url = m[1][0].video_url,
                        user = users.filter(username= post.user.username).get(),
                        comment_count = post.comment_count,
                        like_count = post.like_count,
                        caption_text = post.caption_text,
                        resource = m[0]
                    )
                    p.save()

                elif post.media_type == 1:
                    image = self.download_file(post.thumbnail_url, 1)
                    p = Post(
                        post_id = post.pk,
                        item_id = post.id,
                        media_type = str(post.media_type),
                        thumbnail_url = image,
                        video_url = post.video_url,
                        user = users.filter(username= post.user.username).get(),
                        comment_count = post.comment_count,
                        like_count = post.like_count,
                        caption_text = post.caption_text,
                    )
                    p.save()
                
                elif post.media_type == 2:
                    image = self.download_file(post.thumbnail_url, 1)
                    video = self.download_file(post.video_url, 2)
                    p = Post(
                        post_id = post.pk,
                        item_id = post.id,
                        media_type = str(post.media_type),
                        thumbnail_url = image,
                        video_url = video,
                        user = users.filter(username= post.user.username).get(),
                        comment_count = post.comment_count,
                        like_count = post.like_count,
                        caption_text = post.caption_text,
                    )
                    p.save()

        return redirect('/admin/home/post')

    def create_media(self, post_id:str, resources: List[Resource]):
        res = ResourceFile(
            post_id= post_id
        )
        res.save()

        medias = []
        for item in resources:
            image = self.download_file(item.thumbnail_url, 1)
            video = self.download_file(item.video_url, 2)

            media = MediaFile(
                media_type= str(item.media_type),
                media_id = item.pk,
                thumbnail_url = image,
                video_url = video,
                resource = res
            )
            media.save()
            medias.append(media)
        
        return (res,medias)

    def download_file(self, address: str, media_type: int) -> str:
        if address == None:
            return None

        r = requests.get(address)
        if media_type == 1:
            dir = str(settings.MEDIA_ROOT)
            if not os.path.exists(dir + '/photos/'):
                os.mkdir(dir+ '/photos/')

            name = '/photos/'+str(random.randrange(1000000,1000000000)) + '.jpeg'
            path = dir + name

        elif media_type == 2 :
            dir = str(settings.MEDIA_ROOT)
            if not os.path.exists(dir + '/videos/'):
                os.mkdir(dir+ '/videos/')

            name = '/videos/'+str(random.randrange(1000000,1000000000)) + '.mp4'
            path = dir + name
        
        if r.status_code == 200 :
            file = open(path, 'wb').write(r.content)
            return "/media"+ name
        else :
            return None


class IndexUserList(View):
    def get(self, req):
        users = InstagramPage.objects.all()
        return render(req,'front/users.html',context={
            'users': users
        })


class IndexPostList(View):
    def get(self, req:HttpRequest):
        limit = 50
        offset = 0
        if (req.GET.get('page')):
            offset = (int(req.GET['page']) - 1) * 50
            limit = int(req.GET['page']) * 50
        posts = Post.objects.select_related('resource').select_related('user').all()[offset:limit]
        
        return render(req, 'front/posts.html', context={
            'posts': posts
        })


class PostDetail(View):
    def get(self, req, pk):
        post = Post.objects.select_related('resource').select_related('user').get(pk=pk)
        if post.resource:
            media = MediaFile.objects.filter(resource= post.resource.pk).all()
            post.media_file = media

        return render(req, 'front/post-detail.html',context={
            'post': post
        })


# rest api framework 
class InstagramPost(ReadOnlyModelViewSet):
    queryset = Post.objects.select_related('user').select_related('resource').all()
    serializer_class = PostSerializer


class ResourceItems(ReadOnlyModelViewSet):
    queryset = MediaFile.objects.select_related('resource').all()
    serializer_class = MediaSerializer


class GetResourceMedia(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        return MediaSerializer

    def get_queryset(self):
        return MediaFile.objects.filter(resource_id = self.kwargs['resources_pk'])

    def get_serializer_context(self):
        return {'resource_id': self.kwargs['resources_pk']}


class ReviewViewModel(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(post_id=self.kwargs['posts_pk'])

    def get_serializer_context(self):
        return {'post_id': self.kwargs['posts_pk']}

