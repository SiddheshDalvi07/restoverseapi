from rest_framework import serializers
from .models import Review, Reply

from rest_framework import serializers
from .models import Reply

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'review', 'reply_content']  # Include necessary fields
        read_only_fields = ['review']  # Ensure 'review' is read-only


class ReviewSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'photo_url', 'name', 'date', 'stars', 'content', 'replies')
