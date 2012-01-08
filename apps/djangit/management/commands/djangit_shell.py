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

__all__ = ['Command']

logger = logging.getLogger('djangit.shell')

READONLY_COMMANDS = [
    "git-upload-pack",
    "git upload-pack",
]

class Command(LabelCommand):
    def handle_label(self, username, *args, **options):
        """
        wrap git-shell with djangit repo access check
        """
        user = None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.error("Unknown user.")
            sys.exit(1)

        repo_dir = getattr(settings, 'REPOSITORY_DIRECTORY', None)
        os.chdir(repo_dir) 
        if not repo_dir:
            logger.error("Missing REPOSITORY_DIRECTORY!")
            sys.exit(1)

        git_shell = getattr(settings, 'GIT_SHELL_PATH', 'git-shell')
        ssh_original_command = os.environ.get('SSH_ORIGINAL_COMMAND', None)
        if not ssh_original_command:
            logger.error("Missing SSH_ORIGINAL_COMMAND!")
            sys.exit(1)

        matches = re.match(r"""(?P<command>\S+)\s+'(?P<repo>[^']+)'""", ssh_original_command)
        if not matches:
            logger.error("Unmatched command! '%s'" % (ssh_original_command,))
            sys.exit(1)

        command = matches.group('command')
        repository = matches.group('repo')
        if repository.endswith('.git'):
            repository = repository[:-4]

        if '/' not in repository: # ...
            logger.error("Must specify project_slug/repo_name.")
            sys.exit(1)

        project_slug, repo_name = repository.split('/', 1) 

        qs = None
        try:
            project = Project.objects.get(slug=project_slug)
            qs = project.repo_set.filter(Q(name=repo_name) | Q(aliases__contains=repository))
        except Project.DoesNotExist as e:
            qs = Repo.objects.filter(aliases__contains=repository)

        if len(qs) < 1:
            logger.error("No such repository.")
            sys.exit(1)
        elif len(qs) > 1:
            logger.error("Ambiguous repository?")
            sys.exit(1)
        repo = qs[0]

        access = repo.get_user_access(user)
        if access != RepoMember.ACCESS_WRITABLE:
            if access != RepoMember.ACCESS_READONLY:
                logger.error("Read access denied.")
                sys.exit(1)

            if command not in READONLY_COMMANDS:
                logger.error("Write access denied.")
                sys.exit(1)

        repo_path = '%s.git' % (os.path.join(repo_dir, repo.path),)
        if not os.path.exists(repo_path):
            # if the repo doesn't exist, but is in the models, initialize an empty one
            os.makedirs(repo_path)
            subprocess.call(["git", "--git-dir=.", "init", "--bare"], cwd=repo_path)

        new_command = "%s '%s'" % (command, repo.path)
        logger.debug('rewrote command: "%s" -> "%s"' % (ssh_original_command, new_command,))
        subprocess.call([git_shell, '-c', new_command])
        sys.exit(0)
