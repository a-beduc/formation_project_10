from django.contrib import admin
from softdesk.models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'type')
    list_filter = ('type',)
    search_fields = ('title', 'author')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project')
    search_fields = ('user', 'project')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'project', 'title', 'status', 'priority', 'type')
    list_filter = ('status', 'priority', 'type')
    search_fields = ('author', 'project', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'issue', 'short_content')
    search_fields = ('author', 'issue')

    def short_content(self, obj):
        if obj.content:
            return obj.content[:60] + ("..." if len(obj.content) > 60 else '')
        return ''
