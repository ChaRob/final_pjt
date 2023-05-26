from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from movies.models import Movie, Review
from django.contrib.auth import get_user_model
from movies.serializers import MovieSerializer
# Create your views here.
def ratingnormalization(ratingdict):
    normalized_ratingdict = {}
    if ratingdict:
        minimum = min(ratingdict.values())
        maximum = max(ratingdict.values())
        for rating in ratingdict:
            v = ratingdict[rating] 
            if v > 5.5:
                normalized_ratingdict[rating] = 5.5 + (v - 5.5)*(10-5.5)/(maximum-5.5)
            else:
                normalized_ratingdict[rating] = 5.5 - (5.5 - v)*(5.5-1)/(5.5-minimum)
    return normalized_ratingdict

@api_view(['GET'])
def recommendation_home(request, partycode):
    party = []
    party += [request.user.id]
    answer = []
    already_watched = []
    if partycode != 'alone':
        partycode = partycode.split('-')
        for people in partycode:
            if people:
                if get_user_model().objects.filter(id=request.user.pk, followings=int(people)).exists():
                    party += [int(people)]
    for p in party:
        reviews = Review.objects.filter(user=p)
        ansdict = {}
        reansdict = {}
        for rev in reviews:
            ansdict[rev.movie]=rev.rating
            already_watched += [rev.movie.id]
        ansdict = ratingnormalization(ansdict)
        for ans in ansdict:
            recommendations = Movie.objects.filter(recommendation=ans)
            for recommendation in recommendations:
                try:
                    first = reansdict[recommendation.id][0]
                    last = reansdict[recommendation.id][1]
                    reansdict[recommendation.id] = (ansdict[ans] + first, last + 1)
                except:
                    reansdict[recommendation.id] = (ansdict[ans], 1)
        for reans in reansdict:
            reansdict[reans] = reansdict[reans][0]/reansdict[reans][1]
        answer += [reansdict]
    bigans = {}
    for t in answer:
        for movieid in t:
            try:
                first = bigans[movieid][0]
                last = bigans[movieid][1]
                bigans[movieid] += (t[movieid]+first, last+1)
            except:
                bigans[movieid] = (t[movieid], 1)
    for b in bigans:
        v0 = bigans[b][0]
        v1 = bigans[b][1]
        moviev = Movie.objects.get(id=b)
        bigans[b] = v0 + (len(party)-v1)*moviev.vote_average
    
    tmp = []
    cnt = 0
    for item in sorted(bigans.items(), key=lambda item:-item[1]):
        if item[0] not in already_watched:
            tmp.append(item[0])
            cnt += 1
        if cnt == 6:
            break
    recommend_movie = Movie.objects.filter(id__in=tmp)
    serializer = MovieSerializer(recommend_movie, many=True)
    return Response(serializer.data)
    