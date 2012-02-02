from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from djangit.models import *
import itertools

manager, created = Group.objects.get_or_create(name="manager")
if created:
	_admin_codenames=[p+'_'+s for p in ['add', 'delete', 'change'] for s in ['pubkey', 'repo', 'project', 'projectmember', 'repomember']]
	for p in Permission.objects.filter(codename__in=_admin_codenames):
	    manager.permissions.add(p)
	manager.save()

user, created = Group.objects.get_or_create(name='user')
if created:
	_user_codenames=[p+'_userpubkey' for p in ['add', 'delete', 'change']]
	for p in Permission.objects.filter(codename__in=_user_codenames):
	    user.permissions.add(p)
	user.save()
