from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from djangit.models import Pubkey
from djangit.views import UserRepoListView

urlpatterns = patterns('',
    url(r'^repos/$', UserRepoListView.as_view(), name='user_repos'),
)
