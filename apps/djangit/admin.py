from django.contrib import admin
from djangit.models import *
import basic_models.admin
#import groups so we're sure it's been run
import groups

#used by managers to manage all keys
class PubkeyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','user','comment')
    search_fields = ('user__username',)
    list_filter = ('user',)
admin.site.register(Pubkey, PubkeyAdmin)

class RepoAdmin(admin.ModelAdmin):
    class RepoMemberInline(admin.TabularInline):
        model = RepoMember
        extra = 0
    inlines = (RepoMemberInline,)
    list_display = ('__unicode__','project')
admin.site.register(Repo, RepoAdmin)

class ProjectAdmin(basic_models.admin.DefaultModelAdmin):
    class RepoInline(admin.TabularInline):
        model = Repo
        extra = 0
        fields = ('name','aliases')
    class ProjectMemberInline(admin.TabularInline):
        model = ProjectMember
        extra = 0

    inlines = (RepoInline,ProjectMemberInline)
    list_display = ('__unicode__','slug')
    search_fields = ('slug','name')
admin.site.register(Project, ProjectAdmin)

#used by users to manage their own keys
class UserPubkeyAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('__unicode__','comment')
    search_fields = list_display
    def queryset(self, request):
        return self.model.objects.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
admin.site.register(UserPubkey, UserPubkeyAdmin)
