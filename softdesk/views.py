from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from django_filters import rest_framework as filters

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from softdesk.models import Project, Contributor, Issue, Comment
from softdesk.serializers import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectPostSerializer,
    ContributorListSerializer, ContributorDetailSerializer,
    ContributorPostSerializer,
    IssueListSerializer, IssueDetailSerializer, IssuePostSerializer,
    CommentListSerializer, CommentDetailSerializer, CommentPostSerializer,
)
from softdesk.permissions import (
    IsProjectAuthor, IsProjectContributor, IsResourceAuthor, IsUserContributor
)
from myauth.permissions import IsAdminAuthenticated
from softdesk.filters import (
    ProjectFilterSet, IssueFilterSet, ContributorFilterSet, CommentFilterSet
)

from softdesk.utils import utils


class UtilityViewSet(ModelViewSet):
    """
    This class is inherited by the classes that represent our API
    resources endpoints. The serializer_map, permission_map and
    eventually default_permissions must be implemented in children
    classes.
    """
    serializer_map = {}
    permission_map = {}
    default_permissions = []
    _project_cache = None
    _project_contributors_id_cache = None
    stripped_class_name = ""
    view_name_map = {}
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = None

    def __init_subclass__(cls, **kwargs):
        """
        This method is overwritten after initialization in children
        classes to transform tuple keys in serializer_map and
        permission_map into proper keys with similar values.
        It also creates a map for view_name based on cls.__name__,
        it is used to dynamically modify name displayed by DRF web
        interface.
        """
        super().__init_subclass__(**kwargs)
        cls.serializer_map = utils.flatten_tuple_of_keys(cls.serializer_map)
        cls.permission_map = utils.flatten_tuple_of_keys(cls.permission_map)

        if 'ViewSet' in cls.__name__:
            cls.stripped_class_name = cls.__name__.replace('ViewSet', '')
            cls.view_name_map = {
                'list': f'{cls.stripped_class_name} List',
                'create': f'{cls.stripped_class_name} Create',
                'update': f'{cls.stripped_class_name} Update',
                'partial_update': f'{cls.stripped_class_name} Update',
                'retrieve': f'{cls.stripped_class_name} Detail',
                'destroy': f'{cls.stripped_class_name} Delete',
            }

    def get_serializer_class(self):
        """
        Check for the action performed and if a serializer correspond to
        the action in serializer_map, return it. Otherwise, return a
        default serializer.
        """
        if self.action in self.serializer_map.keys():
            return self.serializer_map[self.action]
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        """
        Return a list of permissions that this view requires. Every
        resources endpoint need at least the [IsAuthenticated]
        permission.
        """
        permission_classes = [IsAuthenticated]
        if self.action in self.permission_map.keys():
            permission_classes += self.permission_map.get(self.action, [])
        else:
            permission_classes += self.default_permissions
        return [permission() for permission in permission_classes]

    def permission_denied(self, request, message=None, code=None):
        """
        Display a custom message when you don't have the required
        authorization to reach a resource endpoint.
        """
        message = "Vous n'avez pas la permission d'accéder à cette ressource."
        super().permission_denied(request, message=message, code=code)

    @property
    def current_project(self):
        """
        Property to cache a Project. It is used by the permissions which
        need to verify elements of the project instance.
        """
        if self._project_cache is None:
            pk = self.kwargs.get('project_pk') or self.kwargs.get('pk')
            self._project_cache = get_object_or_404(Project, pk=pk)
        return self._project_cache

    @property
    def current_project_contributors_id(self):
        """
        Property to cache contributors users id in a set.
        It is used by the permissions which need to verify if a user is
        part of the contributors for a project instance without the need
        for multiple database lookup.
        """
        if self._project_contributors_id_cache is None:
            contributors = self.current_project.contributors.all()
            self._project_contributors_id_cache = {
                contributor.user_id for contributor in contributors
            }
        return self._project_contributors_id_cache

    def get_view_name(self):
        """
        Modify displayed name of view on DRF web interface.
        """
        action = getattr(self, 'action', None)
        return self.view_name_map.get(action, super().get_view_name())


class ProjectViewSet(UtilityViewSet):
    """
    The SoftDesk API is a RESTful API built using Django Rest Framework
    with the objective to develop a secured and efficient backend
    interface to serve different front-end applications. The API uses
    Json Web Token to define access permissions for the resources.

    The Project resource:

    - Allows authenticated users to access the project where they are
    contributor or author.
    - Allows authenticated users to edit the project they are author.
    - Provides basic filtering to search for a specific project.

    An example of usage:

    - To retrieve a list of all projects:
    GET /api/v1/projects/
    - To create a new project:
    POST /api/v1/projects/
    - For a specific project (contributors only):
    GET /api/v1/projects/{{pk}}/
    - To update a project (partial or full, author only):
    PATCH or PUT /api/v1/projects/{{pk}}/
    - To delete a project (author only):
    DELETE /api/v1/projects/{{pk}}/

    If you want to see the list of all the users, please refer to the
    [users endpoint](/api/v1/users/).
    """
    serializer_class = ProjectListSerializer
    serializer_map = {
        'list': ProjectListSerializer,
        'retrieve': ProjectDetailSerializer,
        ('create', 'update', 'partial_update'): ProjectPostSerializer,
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
    filterset_class = ProjectFilterSet

    def get_queryset(self):
        return (Project.objects.all()
                .select_related("author")
                .prefetch_related("contributors__user")
                ).order_by('time_created')

    def perform_create(self, serializer):
        """
        Add the user that created the resource as its author. If a
        resource with the same name created by the same user exist, it
        catches the error sent by the model.
        """
        author = self.request.user

        try:
            serializer.save(author=author)
        except IntegrityError:
            raise ValidationError(
                {'error': "Vous avez déjà créé un projet avec ce nom."}
            )


class ContributorViewSet(UtilityViewSet):
    """
    The SoftDesk API is a RESTful API built using Django Rest Framework
    with the objective to develop a secured and efficient backend
    interface to serve different front-end applications. The API uses
    Json Web Token to define access permissions for the resources.

    The Contributor resource:

    - Allows author to add a new contributor to the project.
    - Allows contributors to delete their own Contributor relation.
    - Provides basic filtering to search for specific contributor.

    An example of usage:

    - To retrieve a list of all contributors:
    GET /api/v1/projects/{{project_pk}}/contributors/
    - To add a new contributor (project author only):
    POST /api/v1/projects/{{project_pk}}/contributors/
    - For a specific contributor (concerned user or project author):
    GET /api/v1/projects/{{project_pk}}/contributors/{{pk}}/
    - To remove a contributor (concerned user or project author):
    DELETE /api/v1/projects/{{project_pk}}/contributors/{{pk}}/
    """
    serializer_class = ContributorListSerializer
    serializer_map = {
        'list': ContributorListSerializer,
        'retrieve': ContributorDetailSerializer,
        'create': ContributorPostSerializer,
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
    filterset_class = ContributorFilterSet

    def get_queryset(self):
        return (Contributor.objects
                .filter(project_id=self.kwargs['project_pk'])
                .select_related('user')
                .select_related('project')).order_by('time_created')

    def perform_create(self, serializer):
        """
        Get the current project from the kwargs dict found in the view :
         {"project_pk":{{int>}
        Try to add a specific user as a contributor to the project,
        if the user is already a contributor, it catches the error sent
        by the model.
        """
        project = Project.objects.get(
            pk=self.kwargs['project_pk']
        )
        user = serializer.validated_data['user']

        try:
            serializer.save(
                project=project,
                user=user
            )
        except IntegrityError:
            raise ValidationError(
                {"error": 'Cet utilisateur est déjà contributeur du projet'}
            )


class IssueViewSet(UtilityViewSet):
    """
    The SoftDesk API is a RESTful API built using Django Rest Framework
    with the objective to develop a secured and efficient backend
    interface to serve different front-end applications. The API uses
    Json Web Token to define access permissions for the resources.

    The Issue resource:

    - Allows project's contributors to add a new issue to the project.
    - Allows issues author to modify their own issue.
    - Allows issue author and the project's author to delete an issue.
    - Provides basic filtering to search for specific issue.

    An example of usage:

    - To retrieve a list of all the issue for a project (project
    contributor only) :
    GET /api/v1/projects/{{project_pk}}/issues/
    - To add a new issue (project contributor only):
    POST /api/v1/projects/{{project_pk}}/issues/
    - For a specific issue (project contributor only):
    GET /api/v1/projects/{{project_pk}}/issues/{{pk}}/
    - To update an issue (partial or full, issue author only):
    PATCH or PUT /api/v1/projects/{{project_pk}}/issues/{{pk}}/
    - To remove an issue (issue author or project author):
    DELETE /api/v1/projects/{{project_pk}}/issues/{{pk}}/
    """
    serializer_class = IssueListSerializer
    serializer_map = {
        'list': IssueListSerializer,
        'retrieve': IssueDetailSerializer,
        ('create', 'update', 'partial_update'): IssuePostSerializer,
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
    filterset_class = IssueFilterSet

    def get_queryset(self):
        return (Issue.objects
                .filter(project_id=self.kwargs['project_pk'])
                .select_related("author")
                .select_related('project')
                .prefetch_related("comments__author")).order_by('time_created')

    def perform_create(self, serializer):
        """
        Get the current project from the kwargs dict found in the view :
         {"project_pk":{{int>}
        If an issue with the same name, for the same project by the same
        author exists, it catches the error sent by the model.
        """
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        author = self.request.user
        try:
            serializer.save(project=project, author=author)
        except IntegrityError:
            raise ValidationError(
                {'error': "Vous avez déjà créé un issue avec ce nom dans ce "
                          "projet."}
            )


class CommentViewSet(UtilityViewSet):
    """
    The SoftDesk API is a RESTful API built using Django Rest Framework
    with the objective to develop a secured and efficient backend
    interface to serve different front-end applications. The API uses
    Json Web Token to define access permissions for the resources.

    The Comment resource:

    - Allows project contributors to add a new comment to the issue.
    - Allows comment author to modify their own comment.
    - Allows comment author and the project's author to delete a
    comment.
    - Provides basic filtering to search for specific contributor.

    An example of usage:

    - To retrieve a list of all the comment for an issue (project
    contributor only) :
    GET /api/v1/projects/{{project_pk}}/issues/{{issue_pk}}/comments/
    - To add a new comment (project contributor only):
    POST /api/v1/projects/{{project_pk}}/issues/{{issue_pk}}/comments/
    - For a specific comment (project contributor only):
    GET
    /api/v1/projects/{{project_pk}}/issues/{{issue_pk}}/comments/{{pk}}/
    - To update a comment (partial or full, comment author only):
    PATCH or PUT
    /api/v1/projects/{{project_pk}}/issues/{{issue_pk}}/comments/{{pk}}/
    - To remove a comment (comment author or project author):
    DELETE
    /api/v1/projects/{{project_pk}}/issues/{{issue_pk}}/comments/{{pk}}/
    """
    serializer_class = CommentListSerializer
    serializer_map = {
        'list': CommentListSerializer,
        'retrieve': CommentDetailSerializer,
        ('create', 'update', 'partial_update'): CommentPostSerializer,
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
    filterset_class = CommentFilterSet

    def get_queryset(self):
        return (Comment.objects
                .filter(issue_id=self.kwargs['issue_pk'])
                .select_related('author')
                .select_related('issue')
                .select_related('issue__project')
                ).order_by('time_created')

    def perform_create(self, serializer):
        """
        Get the current project from the kwargs dict found in the view :
        {"issue_pk":int}
        """
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        author = self.request.user
        serializer.save(issue=issue, author=author)
