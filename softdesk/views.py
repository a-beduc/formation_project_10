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

from softdesk.utils import utils


class UtilityViewSet(ModelViewSet):
    # need to be implemented in children classes
    serializer_map = {}
    permission_map = {}
    default_permissions = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.serializer_map = utils.flatten_tuple_of_keys(cls.serializer_map)
        cls.permission_map = utils.flatten_tuple_of_keys(cls.permission_map)

    def get_serializer_class(self):
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in self.permission_map.keys():
            permission_classes += self.permission_map.get(self.action, [])
        else:
            permission_classes += self.default_permissions
        return [permission() for permission in permission_classes]

    def permission_denied(self, request, message=None, code=None):
        message = "Vous n'avez pas la permission d'accéder à cette ressource."
        super().permission_denied(request, message=message, code=code)


class ProjectViewset(UtilityViewSet):
    serializer_class = ProjectListSerializer
    serializer_map = {
        'list': ProjectListSerializer,
        'retrieve': ProjectDetailSerializer,
        ('update', 'partial_update'): ProjectUpdateSerializer,
        'create': ProjectCreateSerializer,
    }
    permission_map = {
        'retrieve': [
            IsProjectContributor
            | IsAdminAuthenticated
        ],
        ('update', 'partial_update', 'destroy'): [
            IsResourceAuthor
            | IsAdminAuthenticated
        ]
    }

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class ContributorViewset(UtilityViewSet):
    serializer_class = ContributorListSerializer
    serializer_map = {
        'list': ContributorListSerializer,
        'retrieve': ContributorDetailSerializer,
        'create': ContributorCreateSerializer,
    }
    permission_map = {
        'create': [
            IsProjectAuthor
            | IsAdminAuthenticated
        ],
        'destroy': [
            IsUserContributor
            | IsProjectAuthor
            | IsAdminAuthenticated
        ]
    }
    default_permissions = [IsProjectContributor | IsAdminAuthenticated]
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


class IssueViewset(UtilityViewSet):
    serializer_class = IssueListSerializer
    serializer_map = {
        'list': IssueListSerializer,
        'retrieve': IssueDetailSerializer,
        'create': IssueCreateSerializer,
        ('update', 'partial_update'): IssueUpdateSerializer,
    }
    permission_map = {
        ('update', 'partial_update'): [
            IsResourceAuthor
            | IsAdminAuthenticated
        ],
        'destroy': [
            IsResourceAuthor
            | IsProjectAuthor
            | IsAdminAuthenticated
        ]
    }
    default_permissions = [IsProjectContributor | IsAdminAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        author = self.request.user
        serializer.save(project=project, author=author)


class CommentViewset(UtilityViewSet):
    serializer_class = CommentListSerializer
    serializer_map = {
        'list': CommentListSerializer,
        'retrieve': CommentDetailSerializer,
        'create': CommentCreateSerializer,
        ('update', 'partial_update'): CommentUpdateSerializer,
    }
    permission_map = {
        ('update', 'partial_update'): [
            IsResourceAuthor
            | IsAdminAuthenticated
        ],
        'destroy': [
            IsResourceAuthor
            | IsProjectAuthor
            | IsAdminAuthenticated
        ],
    }
    default_permissions = [IsProjectContributor | IsAdminAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        author = self.request.user
        serializer.save(issue=issue, author=author)
