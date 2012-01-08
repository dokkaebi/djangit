

Git Repository Manager
====

Django Web App
-----
- Uses django.contrib.auth User and Groups to manage Projects which contains a set of Repositories.
- Users have the ability to manage their own sets of ssh keys.
- LDAP support via django-auth-ldap.
- Managers can create Projects and grant access to Users or Groups.
- Manage read/write access at Repository or Project level.
- Repositories can have any number of aliases, (to allow for renaming repositories).

Git Shell Wrapper
-----
- Maintains a .ssh/authorized_keys file for a ssh user to allow access (inspired by gitosis)
- Provides a git-shell wrapper as a django manage.py djangit_shell



User Stories
============
    - as a user i can manage my own public keys
    - as a user i can see all the repositories i have access to and their URLs.

    - as a manager i can create new repositories
    - as a manager i can rename/move repositories
    - as a manager i can set up user groups
    - as a manager i can grant/revoke access to a repository for a user/group.

