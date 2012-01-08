from django.db import models

class TeamMemberBase(models.Model):
    ACCESS_READONLY='read'
    ACCESS_WRITABLE='write'
    ACCESS_REVOKED='revoke'
    ACCESS_CHOICES = (
        (ACCESS_READONLY, 'Readonly'),
        (ACCESS_WRITABLE, 'Writable'),
        (ACCESS_REVOKED, 'Revoked'),
    )
    access = models.CharField(max_length=64, choices=ACCESS_CHOICES, default=ACCESS_WRITABLE)
    group = models.ForeignKey("auth.Group", blank=True, null=True)
    user = models.ForeignKey("auth.User", blank=True, null=True)

    class Meta:
        abstract = True