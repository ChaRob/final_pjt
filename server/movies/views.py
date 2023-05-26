from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Review, Genre, BelongstoCollection, ProductionCompanies, Cast, Video, ProductionCountries, Comment
from .models import Boxoffice
from .serializers import BoxofficeSerializer
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewSerializer, CommentSerializer, MovieSerializer
from urllib import parse
from operator import itemgetter
import requests
import datetime
import random
from .secret_key import headers, boxoffice_url_key
    
def save_database(res_id):
    detail_url = f"https://api.themoviedb.org/3/movie/{res_id}?language=ko-KR"
    credits_url = f"https://api.themoviedb.org/3/movie/{res_id}/credits?language=ko-KR"
    recommendation_url = f"https://api.themoviedb.org/3/movie/{res_id}/recommendations?language=ko-KR&page=1"
    similar_url = f"https://api.themoviedb.org/3/movie/{res_id}/similar?language=ko-KR&page=1"
    videos_url = f"https://api.themoviedb.org/3/movie/{res_id}/videos?language=en-US"
    
    movie = Movie.objects.get(id=res_id)
    des = requests.get(detail_url, headers=headers).json()
    crd = requests.get(credits_url, headers=headers).json()
    rec = requests.get(recommendation_url, headers=headers).json()
    sim = requests.get(similar_url, headers=headers).json()
    vid = requests.get(videos_url, headers=headers).json()
    
    if des['belongs_to_collection']:
        try:
            belongs_to_collection = BelongstoCollection(id=des['belongs_to_collection']['id'],
                                                        name=des['belongs_to_collection']['name'],
                                                        poster_path=des['belongs_to_collection']['poster_path'],
                                                        backdrop_path=des['belongs_to_collection']['backdrop_path'])
            belongs_to_collection.save()
        except:
            pass
    else:
        belongs_to_collection = None
        
    for prcom in des['production_companies']:
        try:
            production_companies = ProductionCompanies(id=prcom['id'],
                                                    name=prcom['name'],
                                                    logo_path=prcom['logo_path'])
            production_companies.save()
        except:
            pass
        
    for cst in crd['cast']:
        try:
            cast = Cast(
                        department=cst['known_for_department'],
                        name=cst['name'],
                        profile_path=cst['profile_path'],
                        character=cst['character'],
                        order=cst['order'],
                        credit_id=cst['credit_id']
                        )
            cast.save()
        except:
            pass
    for prcon in des['production_countries']:
        try:
            production_countries = ProductionCountries(name=prcon['name'])
            production_countries.save()
        except:
            pass
        
    
    for vi in vid['results']:
        try:
            video = Video(key=vi['key'])
            video.save()
        except:
            pass    
    
    movie.title=des['title']
    if des['release_date']=="":
        movie.release_date=None
    else:
        movie.release_date=des['release_date']
    movie.poster_path=des['poster_path']        
    movie.vote_average=des['vote_average']
    movie.popularity=des['popularity']
    movie.runtime=des['runtime']
    movie.tagline=des['tagline']
    movie.vote_count=des['vote_count']
    movie.overview=des['overview']
    movie.backdrop_path=des['backdrop_path']
    movie.budget=des['budget']
    movie.revenue=des['revenue']
    movie.belongs_to_collection=belongs_to_collection
    if des['poster_path']:
        movie.save()
        for g in des['genres']:
            movie.genres.add(g['id'])
        for pr in des['production_companies']:
            movie.production_companies.add(pr['id'])
        for prn in des['production_countries']:
            prsave = ProductionCountries.objects.get(name=prn['name'])
            movie.production_countries.add(prsave.id)
        for cc in crd['cast']:
            try:
                ccsave = Cast.objects.get(credit_id=cc['credit_id'])
                movie.cast.add(ccsave.id)
            except:
                pass
        rec_data = sorted(rec['results'], key=itemgetter('popularity', 'vote_average'), reverse=True)
        si_data = sorted(sim['results'], key=itemgetter('popularity', 'vote_average'), reverse=True)
        for recom in rec_data[0:min(len(rec_data), 5)]:
            try:
                movie.recommendation.add(recom['id'])
            except:
                try:
                    movie_for_rec = Movie(id=recom['id'], title=recom['title'], poster_path=recom['poster_path'], release_date=recom['release_date'],
                                    vote_average=recom['vote_average'], popularity=recom['popularity'], vote_count=recom['vote_count'], backdrop_path=recom['backdrop_path'])
                    if recom['poster_path']:
                        movie_for_rec.save()
                        movie.recommendation.add(recom['id'])
                except:
                    pass

        for si in si_data[0:min(len(sim['results']), 5)]:
            try:
                movie.similar.add(si['id'])
            except:
                try:
                    movie_for_si = Movie(id=si['id'], title=si['title'], poster_path=si['poster_path'], release_date=si['release_date'],
                                    vote_average=si['vote_average'], popularity=si['popularity'], vote_count=recom['vote_count'], backdrop_path=recom['backdrop_path'])
                    if si['poster_path']:
                        movie_for_si.save()
                        movie.similar.add(si['id'])
                except:
                    pass
        for vi in vid['results']:
            visave = Video.objects.get(key=vi['key'])
            movie.video.add(visave.id)


def update_database():
    
    print('letsgo')
    genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"

    gen = requests.get(genre_url, headers=headers).json()
    
    for ge in gen['genres']:
            genre = Genre(id=ge['id'], name=ge['name'])
            genre.save()
    
    urlarr = ["https://api.themoviedb.org/3/movie/popular?language=ko-KR&page=",
              "https://api.themoviedb.org/3/movie/top_rated?language=ko-KR&page="
              ]
    
    for ur in urlarr:
        for i in range(1, 2):
            url = ur + str(i)
            res = requests.get(url, headers=headers).json()
            
            for r in res['results']:
                if r['adult'] == False:
                    movie = Movie(id=r['id'])
                    movie.save()
                    save_database(movie.id)


@api_view(['GET'])
def home(request):
    movies = get_list_or_404(Movie.objects.exclude(backdrop_path = None), vote_count__gt=100)
    random.shuffle(movies)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_list_top_rated(request, pk):
    movies= get_list_or_404(Movie.objects.order_by('-vote_average'), vote_count__gt=100)
    serializer = MovieSerializer(movies[12*(pk-1):12*(pk)], many=True)
    context = {
        'data' : serializer.data,
        'totalnum' : len(movies)
    }
    return Response(context)

@api_view(['GET'])
def movie_list_boxoffice(request):
    movies= get_list_or_404(Boxoffice)
    serializer = BoxofficeSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_list_genre(request,genre_id,pk):
    movies = get_list_or_404(Movie.objects.filter(genres=genre_id).order_by('-popularity'), vote_count__gt=100)
    serializer = MovieSerializer(movies[12*(pk-1):12*(pk)], many=True)
    context = {
        'data' : serializer.data,
        'totalnum' : len(movies)
    }
    return Response(context)


@api_view(['GET'])
def movie_list_popular(request, pk):
    movies= get_list_or_404(Movie.objects.order_by('-popularity'), vote_count__gt=100)
    serializer = MovieSerializer(movies[12*(pk-1):12*(pk)], many=True)
    context = {
        'data' : serializer.data,
        'totalnum' : len(movies)
    }
    return Response(context)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
    except:
        movie = Movie(id=movie_pk)
        movie.save()
        save_database(movie_pk)
    if movie.runtime == None:
        save_database(movie_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
        
        
@api_view(['GET'])
def review_list(request, movie_pk):
    reviews = get_list_or_404(Review, movie_id=movie_pk)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        review.delete()
        data = f'review {review_pk} is deleted'
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def comment_list(request, review_pk):
    comments = get_list_or_404(Comment, review_id=review_pk)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.error_messages)

@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'DELETE':
        comment.delete()
        data = f'review {comment_pk} is deleted'
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.error_messages)


@api_view(['POST'])
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def search(request, search_name):
    string_encoded = parse.quote(search_name)
    search_url = f"https://api.themoviedb.org/3/search/movie?query={string_encoded}&include_adult=false&language=ko-KR&page=1"
    search_requests = requests.get(search_url, headers=headers).json()['results']
    search_results = []
    today = str(datetime.datetime.today().date())
    today = today.split('-')
    today = int(''.join(today))
    for search_request in search_requests:
        release_date = search_request['release_date']
        if release_date:
            release_date = str(release_date).split('-')
            release_date = int("".join(release_date))
            if release_date < today:
                dt = {  'id':search_request['id'],
                        'title':search_request['title'],
                        'overview':search_request['overview'],
                        'vote_average':search_request['vote_average'],
                        'release_date':search_request['release_date'],
                        'poster_path':search_request['poster_path'],
                        'vote_count':search_request['vote_count'],
                        'backdrop_path':search_request['backdrop_path']
                        }
                if search_request['poster_path']:
                    search_results += [dt]
                    if not Movie.objects.filter(id=dt['id']).exists():
                        savemovie = Movie(
                            id=dt['id'],
                            title=dt['title'],
                            overview=dt['overview'],
                            vote_average=dt['vote_average'],
                            release_date=dt['release_date'],
                            poster_path=dt['poster_path'],
                            vote_count=search_request['vote_count'],
                            backdrop_path=search_request['backdrop_path'],
                            popularity=search_request['popularity']
                            )
                        savemovie.save()
                        for genre in search_request['genre_ids']:
                            savemovie.genres.add(genre)
    return Response({ 'search_results':search_results })


def update_boxoffice():
    print('야호')
    boxoffice = Boxoffice.objects.all()
    boxoffice.delete()
    today = int(str(datetime.datetime.now().date()).replace('-',''))-1
    boxoffice_url = boxoffice_url_key + str(today)
    b_requests = requests.get(boxoffice_url).json()['boxOfficeResult']['dailyBoxOfficeList']
    for box in b_requests:
        movienm = box['movieNm']
        if movienm[-1].isdigit():
            if not movienm[-2].isdigit() and movienm[-2] != " ":
                head = movienm[0:-1]
                tail = movienm[-1]
                movienm = head + ' ' + tail
        string_encoded = parse.quote(movienm)
        search_url = f"https://api.themoviedb.org/3/search/movie?query={string_encoded}&include_adult=false&language=ko-KR&page=1"
        search_requests = requests.get(search_url, headers=headers).json()['results'][0]
        newmov = Movie(id=search_requests['id'])
        newmov.save()
        save_database(search_requests['id'])
        boxoffice = Boxoffice(movie = Movie.objects.get(id=search_requests['id']),
                            rank=box['rank'],
                            rank_inten=box['rankInten'],
                            open_dt=box['openDt'],
                            audicnt=box['audiCnt'],
                            audiacc=box['audiAcc'])
        boxoffice.save()
        
@api_view(['GET'])
def main(request):
    boxoffices = get_list_or_404(Boxoffice)
    serializer = BoxofficeSerializer(boxoffices, many=True)
    return Response(serializer.data)
