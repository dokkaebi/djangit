import os
import re
import subprocess
import sys
import logging

from django.core.management.base import LabelCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from djangit.models import *

logger = logging.getLogger('djangit.shell')


class Command(LabelCommand):
    def handle_label(self, username, *args, **options):
        """
        wrap git-shell with djangit repo access check
        """
        user = None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            sys.exit(1)

        repo_dir = getattr(settings, 'REPOSITORY_DIRECTORY', None)
        os.chdir(repo_dir) 
        if not repo_dir:
            sys.exit(1)

        git_shell = getattr(settings, 'GIT_SHELL_PATH', 'git-shell')
        ssh_original_command = os.environ.get('SSH_ORIGINAL_COMMAND', None)
        if not ssh_original_command:
            sys.exit(1)


        matches = re.match(r"""(?P<command>\S+)\s+'(?P<repo>[^']+)'""", ssh_original_command)
        if not matches:
            sys.exit(1)

        cmd = matches.group('command')
        repository = matches.group('repo')
        if repository.endswith('.git'):
            repository = repository[:-4]

        if '/' not in repository: # ...
            sys.exit(1)

        project_slug, repo_name = repository.split('/', 1) 


        qs = None
        try:
            project = Project.objects.get(slug=project_slug)
            qs = project.repo_set.filter(Q(name=repo_name) | Q(aliases__contains=repsitory))
        except Project.DoesNotExist as e:
            qs = Repo.objects.filter(aliases__contains=repository)

        if len(qs) < 1:
            sys.exit(1)
        repo = qs[0] # FIXME

        if not repo.user_has_access(user):
            sys.exit(1)

        new_command = "%s '%s'" % (cmd, repo.path)
        logger.debug('djangit.shell:rewrote command: "%s" -> "%s"' % (ssh_original_command, new_command,))
        subprocess.call([git_shell, '-c', new_command])
        sys.exit(0)
