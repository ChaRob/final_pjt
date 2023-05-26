from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Review, Movie

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"

class InfoSerializer(serializers.ModelSerializer):
    
    # class FollowingsSerializer(serializers.ModelSerializer):
        
    #     class Meta:
    #         model = get_user_model()
    #         fields = "__all__"
    # followers = FollowingsSerializer(many=True, read_only=True)

    class FollowersSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = get_user_model()
            fields = "__all__"
    followers = FollowersSerializer(many=True, read_only=True)
    followings = FollowersSerializer(many=True, read_only=True)

    class ReviewTCSerializer(serializers.ModelSerializer):
        
        class MovieTCSerializer(serializers.ModelSerializer):
            class Meta:
                model = Movie
                fields = "__all__"

        movie = MovieTCSerializer(read_only=True)
        user = UserSerializer(read_only=True)
        class Meta:
            model = Review
            fields = "__all__"
            
    review_set = ReviewTCSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = "__all__"
    

class ProfileSerializer(serializers.ModelSerializer):
    
    profile_image = serializers.ImageField(use_url=True, required=False)    
    class Meta:
        model = get_user_model()
        # fields = "__all__"
        fields = ('intro','email','profile_image',)
        read_only_fields = ('id','password','username','followings',)