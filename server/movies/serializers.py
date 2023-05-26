from rest_framework import serializers
from .models import Movie, Review, Genre, BelongstoCollection, ProductionCompanies, ProductionCountries, Cast, Video, Comment, Boxoffice
from accounts.serializers import UserSerializer

class BelongstoCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BelongstoCollection
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = "__all__"

class ProductionCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompanies
        fields = "__all__"

class ProductionCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountries
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    
    belongs_to_collection = BelongstoCollectionSerializer(read_only=True)
    cast = CastSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    production_companies = ProductionCompaniesSerializer(many=True, read_only=True)
    production_countries = ProductionCountriesSerializer(many=True, read_only=True)
    video = VideoSerializer(many=True, read_only=True)
    
    class RecommendationSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ("id","title","release_date","vote_average","poster_path",)
    recommendation = RecommendationSerializer(many=True, read_only=True)

    class SimilarSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ("id","title","release_date","vote_average","poster_path",)
    similar = SimilarSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = "__all__"

    
class CommentSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class BoxofficeSerializer(serializers.ModelSerializer):
    
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Boxoffice
        fields = "__all__"
        
        
