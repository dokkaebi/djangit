from django.views.generic import ListView, DetailView
from mainsite.views import LoginRequiredMixin
from djangit.models import *

class UserRepoListView(LoginRequiredMixin, ListView):
    model=ProjectMember
    context_object_name='project_members'
    template_name='djangit/user_repos.html'

    def get_queryset(self):
        return ProjectMember.objects.select_related(depth=2).filter(user=self.request.user)
