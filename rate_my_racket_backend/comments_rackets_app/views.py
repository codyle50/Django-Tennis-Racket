from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

import json

import math 

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from knox.models import AuthToken

from .models import *
from .serializers import *


from .models import *

from accounts_app.models import UserProfile


# Create your views here.

class BrandListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = BrandSerializer
    model = Brand
    queryset = Brand.objects.all()



class RacketListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RacketSerializer
    model = Racket
    queryset = Racket.objects.all().order_by("-points")


class TopPrincipalRatedView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RacketSerializer
    model = Racket
    queryset = Racket.objects.all().order_by("-points")[:3]


class BrandRetriveView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = BrandAllRacketsSerializer
    model = Brand
    lookup_url_kwarg = 'brand_id'
    queryset = Brand.objects.all()



class RacketRetriveView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RacketDetailsSerializer
    model = Racket
    lookup_url_kwarg = 'racket_id'
    queryset = Racket.objects.all()


class CategoriesListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = CategoryRatingRacketsSerializer
    model = CategoryRating
    queryset = CategoryRating.objects.all()




# ============================================================
#               BEGIN HELPER
# ============================================================

def updateRatingProp(overall_rating_name, amount_of_votes, new_rating, racket):
    if(new_rating < 11):
        category = CategoryRating.objects.get(title=overall_rating_name)
        try:
            overall_rating_prop = OverallRacketRating.objects.get(category=category, racket=racket)
        except:
            overall_rating_prop = OverallRacketRating(category=category, racket=racket)
            overall_rating_prop.save()
        
        overall_rating_prop.rating = (overall_rating_prop.rating * amount_of_votes + new_rating) / (amount_of_votes + 1)
        overall_rating_prop.points = overall_rating_prop.points + math.sqrt(new_rating)
        overall_rating_prop.save()



# ============================================================
#               END HELPER
# ============================================================

class CreateCommentView(APIView):

    def post(self, request, racket_id, userprofile_id):

        data = request.data

        racket = Racket.objects.get(id=racket_id)
        user = User.objects.get(id=userprofile_id)
        userprofile = user.userprofile

        try:
            rating_comment = RatingComment.objects.get(userprofile=userprofile, racket=racket)
            return Response({"Result": "User already has comment on this racket"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            rating_comment = RatingCommentSerializer(data=data)

            if rating_comment.is_valid() == False:
                return Response({"Result": "Error while creating comment"}, status=status.HTTP_400_BAD_REQUEST)

            rating_comment = rating_comment.save()
            rating_comment.userprofile = userprofile
            rating_comment.racket = racket
            rating_comment.save()

            if(rating_comment.overall_rating < 11):

                racket_new_rating = ((racket.overall_rating * racket.amount_of_votes) + (rating_comment.overall_rating)) / (racket.amount_of_votes + 1)

                racket.overall_rating = racket_new_rating
                racket.amount_of_votes = racket.amount_of_votes + 1
                racket.points = racket_new_rating * racket_new_rating * (racket.amount_of_votes + 1)
                racket.save()

            updateRatingProp("Spin", racket.amount_of_votes-1, rating_comment.spin_rating, racket)
            updateRatingProp("Maneuverability", racket.amount_of_votes-1, rating_comment.maneuverable_rating, racket)
            updateRatingProp("Flexibility", racket.amount_of_votes-1, rating_comment.flexibility_rating, racket)
            updateRatingProp("Comfort", racket.amount_of_votes-1, rating_comment.comfort_rating, racket)
            updateRatingProp("Control", racket.amount_of_votes-1, rating_comment.control_rating, racket)
            updateRatingProp("Power", racket.amount_of_votes-1, rating_comment.power_rating, racket)
            updateRatingProp("During Service", racket.amount_of_votes-1, rating_comment.serving_rating, racket)
            updateRatingProp("During Volley", racket.amount_of_votes-1, rating_comment.volley_rating, racket)
            updateRatingProp("Sweet Spot", racket.amount_of_votes-1, rating_comment.racket_sweet_spot_rating, racket)
            updateRatingProp("Stability", racket.amount_of_votes-1, rating_comment.stable_rating, racket)

            if data['audience'] != "Don't Know":

                category = CategoryRating.objects.get(title=data['audience'])
                try:
                    overall_rating_prop = OverallRacketRating.objects.get(category=category, racket=racket)
                except:
                    overall_rating_prop = OverallRacketRating(category=category, racket=racket)
                    overall_rating_prop.save()
                
                overall_rating_prop.rating = 0
                overall_rating_prop.points = 1
                overall_rating_prop.save()

            return Response({"Result": "Success"}, status=status.HTTP_200_OK)



class LatestCommentsView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = LatestRatesCommentsSerializer
    model = RatingComment
    queryset = RatingComment.objects.all().order_by('-pk')[:3]


class CreateUpdateVote(APIView):

    def post(self, request, comment_id, userprofile_id):

        data = request.data

        rating_comment = RatingComment.objects.get(id=comment_id)

        user = User.objects.get(id=userprofile_id)
        userprofile = user.userprofile

        try:
            vote_for_comment = RatingCommentVote.objects.get(userprofile=userprofile, rating_comment=rating_comment)
            if vote_for_comment.vote_type != data['vote_type'] and vote_for_comment.vote_type != "NO VOTE" :
                vote_for_comment.vote_type = data['vote_type']
                vote_for_comment.save()
                # Remove previous voting
                if(data['vote_type'] == "UP_VOTE"):
                    rating_comment.amounts_of_down_votes = rating_comment.amounts_of_down_votes - 1
                else:
                    rating_comment.amounts_of_up_votes = rating_comment.amounts_of_up_votes - 1
                rating_comment.save()
            elif (vote_for_comment.vote_type == data['vote_type']):
                return Response({"Result": "User already has made this vote"}, status=status.HTTP_400_BAD_REQUEST)
        except :
            vote_for_comment = RatingCommentVote(userprofile=userprofile, rating_comment=rating_comment, vote_type=data['vote_type'])
        vote_for_comment.save()

        if(data['vote_type'] == "UP_VOTE"):
            rating_comment.amounts_of_up_votes = rating_comment.amounts_of_up_votes + 1
        else:
            rating_comment.amounts_of_down_votes = rating_comment.amounts_of_down_votes + 1
        rating_comment.save()

        return Response({"Result": "Success"}, status=status.HTTP_200_OK)


class CategoryRetrieveView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = CategoryRatingRacketsDetailSerializer
    model = CategoryRating
    lookup_url_kwarg = 'category_id'
    queryset = CategoryRating.objects.all()









# ============================================================
#               BEGIN HELPER
# ============================================================

def updateTopRatingProp(category, amount_of_points, racket):
    try:
        overall_rating_prop = OverallRacketRating.objects.get(category=category, racket=racket)
    except:
        overall_rating_prop = OverallRacketRating(category=category, racket=racket)
        overall_rating_prop.save()
        
    overall_rating_prop.points = overall_rating_prop.points + amount_of_points
    overall_rating_prop.save()



# ============================================================
#               END HELPER
# ============================================================





class TopRacketsCategoryCreateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, category_id, userprofile_id):

        data = request.data

        category = CategoryRating.objects.get(id=category_id)
        user = User.objects.get(id=userprofile_id)
        userprofile = user.userprofile

        try:
            top_rackets_category = TopRacketCategory.objects.get(category=category, userprofile=userprofile)
            return Response({"Result": "Error, user already has top rackets for this category"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            top_rackets_category = TopRacketCategory(category=category, userprofile=userprofile)
            top_rackets_category.save()

            gold_racket_id = data['gold_racket_id']
            gold_racket = Racket.objects.get(id=gold_racket_id)
            silver_racket_id = data['silver_racket_id']
            silver_racket = Racket.objects.get(id=silver_racket_id)
            bronze_racket_id = data['bronze_racket_id']
            bronze_racket = Racket.objects.get(id=bronze_racket_id)

            top_rackets_category.gold_racket = gold_racket
            top_rackets_category.silver_racket = silver_racket
            top_rackets_category.bronze_racket = bronze_racket
            top_rackets_category.save()

            updateTopRatingProp(category, 15, gold_racket)
            updateTopRatingProp(category, 10, silver_racket)
            updateTopRatingProp(category, 8, bronze_racket)

            return Response({"Result": "Success"}, status=status.HTTP_200_OK)





class RacketUserListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RacketSerializer
    model = Racket

    def get_queryset(self):
        userprofile_id = self.kwargs.get("userprofile_id")
        user = User.objects.get(id=userprofile_id)
        userprofile = user.userprofile
        rackets = Racket.objects.filter(rating_comment__userprofile=userprofile)
        return rackets


class TopRacketUserListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = TopRacketCategorySerializer
    model = TopRacketCategory

    def get_queryset(self):
        userprofile_id = self.kwargs.get("userprofile_id")
        user = User.objects.get(id=userprofile_id)
        userprofile = user.userprofile
        top_racket_category = TopRacketCategory.objects.filter(userprofile=userprofile)
        return top_racket_category
