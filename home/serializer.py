import resource
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import Post, ResourceFile, MediaFile, Review


class MediaSerializer(ModelSerializer):
    class Meta:
        model =  MediaFile
        fields = '__all__'


class ResourceSerializer(ModelSerializer):
    class Meta:
        model= ResourceFile
        fields = ['post_id','resource']

    resource = serializers.SerializerMethodField(method_name='medias')
    
    def medias(self, resource):
        medias = MediaFile.objects.select_related('resource').filter(resource= resource.pk)
        return MediaSerializer(medias, many=True).data


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    resource = ResourceSerializer()


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['pk', 'username', 'post', 'content', 'date']

    def create(self, validated_data):
        return Review.objects.create(post_id= self.context['post_id'], **validated_data)