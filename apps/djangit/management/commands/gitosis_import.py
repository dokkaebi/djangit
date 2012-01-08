import ConfigParser
import os
import sys
import re

from django.core.management.base import LabelCommand, CommandError

from django.contrib.auth.models import User
from djangit.models import *



class Command(LabelCommand):
    def handle_label(self, label, **options):
        cfg = ConfigParser.ConfigParser()
        cfg.read(label)
        keydir = os.path.join(os.path.dirname(label), 'keydir')

        ##
        # parse the gitosis.conf into indexes
        ##
        users = {}
        groups = {}
        repos = {}
        for section in cfg.sections():
            sect = dict(cfg.items(section))
            grp = section.replace('group ','')

            if grp not in groups:
                groups[grp] = {
                    'members': [],
                    'writable': [],
                }
            for repo in re.split(r'\s+', sect.get('writable','')):
                if repo:
                    groups[grp]['writable'].append(repo)

                    if '/' in repo:
                        dpt,reponame = repo.split('/')
                    else:
                        dpt,reponame = '-',repo

                    if dpt not in repos:
                        repos[dpt] = {}

                    if reponame not in repos[dpt]:
                        repos[dpt][reponame] = {
                            'groups': [],
                        }
                    repos[dpt][reponame]['groups'].append(grp)

            for member in re.split(r'\s+', sect.get('members','')):
                if member not in groups[grp]['members']:
                    groups[grp]['members'].append(member)

                if member not in users:
                    users[member] = {
                        'groups': [],
                        'writable': [],
                    }
                if grp not in users[member]['groups']:
                    users[member]['groups'].append(grp)

                for repo in re.split(r'\s+', sect.get('writable','')):
                    if repo:
                        users[member]['writable'].append(repo)
         
        ##
        # update django models from indexes
        ##
        for group_name,group in groups.items():
            proj, created = Project.objects.get_or_create(slug=group_name)
            if created:
                proj.name = group_name
                proj.save()

            for member_name in group['members']:
                user, created = User.objects.get_or_create(username=member_name)

                keypath = os.path.join(keydir, '%s.pub' % (member_name,))
                if os.path.exists(keypath):
                    with open(keypath, 'r') as fh:
                        comment = ''
                        for key in fh.readlines():
                            key = key.strip()
                            if key.startswith('#'):
                                comment = key
                                continue
                            if key:
                                pubkey, created = Pubkey.objects.get_or_create(user=user, key=key)
                                if created and comment:
                                    pubkey.comment = comment
                                    pubkey.save()
                                    comment = ''

                pm, created = ProjectMember.objects.get_or_create(project=proj, user=user)

            for repo_name in group['writable']:
                repo, created = Repo.objects.get_or_create(project=proj, name=repo_name)



       


