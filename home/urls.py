from django.urls import path, include
from .views import IndexUserList, GetInstagramPosts, InstagramPost, ResourceItems, IndexPostList, PostDetail
from . import views
from rest_framework_nested import routers

route = routers.DefaultRouter()
route.register('posts', InstagramPost)
route.register('resource', ResourceItems)

review = routers.NestedDefaultRouter(route, 'posts', lookup='posts')
review.register('reviews', views.ReviewViewModel, basename='posts-reviews')

resource = routers.NestedDefaultRouter(route, 'resource', lookup='resources')
resource.register('media', views.GetResourceMedia, basename='media-resource')

urlpatterns = [
    path('get-posts',GetInstagramPosts.as_view()),
    path('',IndexUserList.as_view()),
    path('posts',IndexPostList.as_view()),
    path('posts/<int:pk>',PostDetail.as_view()),
    path('api/',include(review.urls)),
    path('api/',include(resource.urls)),
    path('api/', include(route.urls))
]
