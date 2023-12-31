from django.urls import re_path as url,include
from .views import *
from knox import views as knox_views

app_name = 'comments_rackets_app'

urlpatterns = [
    url(r'^brands/$', BrandListView.as_view(), name='brand-list-api'),
    url(r'^top-principal-rated/$', TopPrincipalRatedView.as_view(), name='top-principal-rated-api'),
    url(r'^brand-rackets/(?P<brand_id>\d+)/$', BrandRetriveView.as_view(), name='brand-rackets-api'),
    url(r'^racket/(?P<racket_id>\d+)/$', RacketRetriveView.as_view(), name='racket-api'),
    url(r'^create-comment/(?P<racket_id>\d+)/(?P<userprofile_id>\d+)/$', CreateCommentView.as_view(), name='create-comment-api'),
    url(r'^latest-comments/$', LatestCommentsView.as_view(), name='latest-comments-api'),
    url(r'^create-vote/(?P<comment_id>\d+)/(?P<userprofile_id>\d+)/$', CreateUpdateVote.as_view(), name='create-vote-api'),
    url(r'^categories/$', CategoriesListView.as_view(), name='categories-api'),
    url(r'^category-rackets/(?P<category_id>\d+)/$', CategoryRetrieveView.as_view(), name='category-rackets-api'),
    url(r'^rackets/$', RacketListView.as_view(), name='rackets-list-api'),
    url(r'^rate-top_rackets/(?P<category_id>\d+)/(?P<userprofile_id>\d+)/$', TopRacketsCategoryCreateView.as_view(), name='rate-top-rackets-api'),
    url(r'^user-rated-rackets/(?P<userprofile_id>\d+)/$', RacketUserListView.as_view(), name='user-rated-rackets-api'),
    url(r'^top-rackets-category/(?P<userprofile_id>\d+)/$', TopRacketUserListView.as_view(), name='top-rackets-category-api'),
]