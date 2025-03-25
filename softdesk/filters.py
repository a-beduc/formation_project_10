from django_filters import rest_framework as filters
from softdesk.models import Project, Issue, Contributor, Comment


class ProjectFilterSet(filters.FilterSet):
    """
    Implements filters to be used with the project-list endpoint.
    """
    project_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iexact'
    )
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="iexact"
    )
    title_contains = filters.CharFilter(
        field_name="title",
        lookup_expr='icontains'
    )
    author_id = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='iexact',
    )
    my_projects = filters.BooleanFilter(
        label='my project :',
        method='filter_my_project'
    )

    def filter_my_project(self, queryset, name, value):
        """
        Filter query to only keep the projects where the user is a
        contributor.
        NB : If a user is the project's author, he will always be a
        contributor.
        """
        if value:
            user = self.request.user
            queryset = queryset.filter(contributors__user=user)
        return queryset

    class Meta:
        model = Project
        fields = [
            'project_id',
            'title',
            'title_contains',
            'type',
            'author_id',
            'my_projects'
        ]


class IssueFilterSet(filters.FilterSet):
    """
    Implements filters to be used with the project-issue-list endpoint.
    """
    issue_id = filters.NumberFilter(
        field_name='id',
        lookup_expr='iexact'
    )
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="iexact"
    )
    title_contains = filters.CharFilter(
        field_name="title",
        lookup_expr='icontains'
    )
    author_id = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )
    assigned_to = filters.NumberFilter(
        field_name='assigned_to__id',
        lookup_expr='exact'
    )

    class Meta:
        model = Issue
        fields = [
            'issue_id',
            'title',
            'title_contains',
            'author_id',
            'assigned_to',
            'priority',
            'type',
            'status'
        ]


class ContributorFilterSet(filters.FilterSet):
    """
    Implements filters to be used with the project-contributor-list endpoint.
    """
    user_id = filters.NumberFilter(
        field_name='user__id',
        lookup_expr='iexact'
    )

    class Meta:
        model = Contributor
        fields = ['user_id']


class CommentFilterSet(filters.FilterSet):
    """
    Implements filters to be used with the issue-comment-list endpoint.
    """
    author_id = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='iexact'
    )

    class Meta:
        model = Comment
        fields = ['author_id']
