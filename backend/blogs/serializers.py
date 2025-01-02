from rest_framework import serializers
from .models import Blog, Like, Comment

# Define the CommentSerializer first
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name',read_only=True)  # Or 'user' if you want more user details

    class Meta:
        model = Comment
        fields = ['id', 'content', 'status','created_at','user']
        read_only_fields = ['status', 'created_at','user']


# Define the BlogSerializer after CommentSerializer
class BlogSerializer(serializers.ModelSerializer):
    liked_by_user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'image', 'attachment', 'created_at', 'updated_at', 'liked_by_user', 'likes_count', 'comments']

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(user=user).exists()

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'blog', 'created_at']
