from rest_framework import serializers
from asset.serializers import AssetSerializer
from authentication.serializers import UserSerializer
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['asset'] = AssetSerializer()
        self.fields['user'] = UserSerializer()
        return super().to_representation(instance)


class PostCreateSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'caption', 'user', 'asset', 'status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
