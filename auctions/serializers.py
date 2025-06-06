from rest_framework import serializers
from .models import *

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = '__all__'  # Ou liste campos específicos: ['id', 'title', ...]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        # Garante que a senha seja criptografada
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

class CreateListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "bidstart", "urlImage", "category"]
    
    def create(self, validated_data):
        validated_data['createdBy'] = self.context['request'].user
        return AuctionListing.objects.create(**validated_data)
    
class WatchlistAddAuctionSerializer(serializers.Serializer):
    class Meta:
        model = Watchlist
        fields = ["user", "item"]
    
    def create(self, validated_data):
        validated_data['createdBy'] = self.context['request'].user
        