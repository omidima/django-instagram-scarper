from django.urls import path, include
from .views import IndexUserList ,getInstagramPosts, InstagramPost, ResourceItems, IndexPostList,PostDetail
from rest_framework import routers

route = routers.DefaultRouter()
route.register('posts',InstagramPost)
route.register('resource',ResourceItems)

urlpatterns = [
    path('get-posts',getInstagramPosts.as_view()),
    path('',IndexUserList.as_view()),
    path('posts',IndexPostList.as_view()),
    path('posts/<int:pk>',PostDetail.as_view()),
    path('api/', include(route.urls))
]
