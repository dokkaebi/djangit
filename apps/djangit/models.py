from django.db import models

from basic_models import models as basic_models
from mainsite.models import TeamMemberBase



from hashlib import md5



class Pubkey(basic_models.DefaultModel):
    user = models.ForeignKey("auth.User")
    key = models.TextField()
    comment = models.TextField(blank=True)

    @property
    def key_ident(self):
        return self.key.split(' ')[-1]

    def __unicode__(self):
        return self.key_ident


class Project(basic_models.SlugModel):
    pass

class ProjectMember(TeamMemberBase):
    project = models.ForeignKey(Project)

class Repo(basic_models.DefaultModel):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=1024)
    aliases = models.CharField(max_length=4096, blank=True)

    @property
    def path(self):
        return '%s/%s' % (self.project.slug, self.name)

    def __unicode__(self):
        return self.path

    def get_user_access(self, user):
        user_groups = user.groups.all()
        qs = self.project.projectmember_set.filter(
            models.Q(user=user) | 
            models.Q(group__in=user.groups.all())
        )
        for rec in qs:
            if rec.access in (ProjectMember.ACCESS_WRITABLE,ProjectMember.ACCESS_READONLY):
                return rec.access
        return None

class RepoMember(TeamMemberBase):
    repo = models.ForeignKey(Repo)
