from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

# detail
class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
class BelongstoCollection(models.Model):
    name = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200, null=True)
    backdrop_path=models.CharField(max_length=200, null=True)

class ProductionCompanies(models.Model):
    logo_path = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=50, null=True)
    
class ProductionCountries(models.Model):
    name = models.CharField(max_length=80, unique=True)


# cast
class Cast(models.Model):
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    profile_path = models.CharField(max_length=200, null=True)
    character = models.CharField(max_length=100, null=True)
    order = models.IntegerField()
    credit_id = models.CharField(max_length=100, unique=True)
#video
class Video(models.Model):
    key = models.CharField(max_length=100, unique=True)

class Movie(models.Model):
    title = models.CharField(max_length=100, null=True)
    release_date = models.DateField(null=True)
    runtime = models.IntegerField(null=True)
    tagline = models.CharField(max_length=80, null=True)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    overview = models.TextField(null=True)
    poster_path = models.CharField(max_length=200,null=True)
    backdrop_path = models.CharField(max_length=200,null=True)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)
    belongs_to_collection = models.ForeignKey(BelongstoCollection, null=True, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(ProductionCompanies)
    production_countries = models.ManyToManyField(ProductionCountries)
    cast = models.ManyToManyField(Cast)    
    recommendation = models.ManyToManyField('self',symmetrical=False, related_name='recommended')
    similar = models.ManyToManyField('self', symmetrical=False, related_name='similar_from')
    video = models.ManyToManyField(Video)

class Review(models.Model):
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users', blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)])

class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Boxoffice(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.PROTECT, primary_key=True)
    rank = models.IntegerField()
    rank_inten = models.CharField(max_length=10)
    open_dt = models.CharField(max_length=20)
    audicnt = models.IntegerField()
    audiacc = models.IntegerField()

