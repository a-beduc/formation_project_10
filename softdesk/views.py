from rest_framework.viewsets import ModelViewSet

from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  ContributorSummarySerializer, ContributorListSerializer, ContributorDetailSerializer,
                                  IssueListSerializer, IssueDetailSerializer,
                                  CommentListSerializer, CommentDetailSerializer)


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    query_set = Project.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return self.query_set

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class CommentViewset(ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()
