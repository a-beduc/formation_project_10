from django.db import IntegrityError

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectCreateSerializer, ProjectUpdateSerializer,
    ContributorListSerializer, ContributorDetailSerializer, ContributorCreateSerializer,
    IssueListSerializer, IssueDetailSerializer, IssueCreateSerializer, IssueUpdateSerializer,
    CommentListSerializer, CommentDetailSerializer, CommentCreateSerializer, CommentUpdateSerializer
)
from softdesk.permissions import IsProjectAuthor, IsProjectContributor, IsResourceAuthor, IsUserContributor
from myauth.permissions import IsAdminAuthenticated


class UtilityViewSet(ModelViewSet):
    # need to be implemented in children classes
    serializer_map = {}
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()


class ProjectViewset(UtilityViewSet):
    serializer_class = ProjectListSerializer
    serializer_map = {
        'list': ProjectListSerializer,
        'retrieve': ProjectDetailSerializer,
        'update': ProjectUpdateSerializer,
        'create': ProjectCreateSerializer,
        'partial_update': ProjectUpdateSerializer,
    }

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [
                (IsAuthenticated & IsResourceAuthor)
                | IsAdminAuthenticated
            ]
        elif self.action in ['retrieve']:
            self.permission_classes = [
                (IsAuthenticated & IsProjectContributor)
                | IsAdminAuthenticated
            ]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class ContributorViewset(UtilityViewSet):
    serializer_class = ContributorListSerializer
    serializer_map = {
        'list': ContributorListSerializer,
        'retrieve': ContributorDetailSerializer,
        'create': ContributorCreateSerializer,
    }
    http_method_names = ['get', 'post', 'delete', 'options', 'head']

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        user = serializer.validated_data['user']

        try:
            serializer.save(project=project, user=user)
        except IntegrityError:
            raise ValidationError({"error": 'Cet utilisateur est déjà contributeur du projet'})

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [
                (IsAuthenticated & IsProjectAuthor)
                | IsAdminAuthenticated
            ]
        elif self.action == 'destroy':
            self.permission_classes = [
                (IsAuthenticated & IsUserContributor)
                | (IsAuthenticated & IsProjectAuthor)
                | IsAdminAuthenticated
            ]
        else:
            self.permission_classes = [
                (IsAuthenticated & IsProjectContributor)
                | IsAdminAuthenticated
            ]
        return [permission() for permission in self.permission_classes]


class IssueViewset(UtilityViewSet):
    serializer_class = IssueListSerializer
    serializer_map = {
        'list': IssueListSerializer,
        'retrieve': IssueDetailSerializer,
        'create': IssueCreateSerializer,
        'partial_update': IssueUpdateSerializer,
        'update': IssueUpdateSerializer,
    }

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)


class CommentViewset(UtilityViewSet):
    serializer_class = CommentListSerializer
    serializer_map = {
        'list': CommentListSerializer,
        'retrieve': CommentDetailSerializer,
        'create': CommentCreateSerializer,
        'partial_update': CommentUpdateSerializer,
        'update': CommentUpdateSerializer,
    }

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(issue=issue)
