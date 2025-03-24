from rest_framework.serializers import (
    ModelSerializer, HyperlinkedIdentityField, PrimaryKeyRelatedField
)
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from myauth.serializers import UserSummarySerializer
from softdesk.models import Project, Issue, Contributor, Comment
from myauth.models import User


class ContributorListSerializer(ModelSerializer):
    """
    Serializer for the Contributor model. Minimal info + a link to the
    detailed view.
    """
    user = UserSummarySerializer(read_only=True)
    contributor_detail = NestedHyperlinkedIdentityField(
        view_name='project-contributor-detail',
        parent_lookup_kwargs={'project_pk': 'project__pk'},
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'contributor_detail',
        ]


class ContributorDetailSerializer(ModelSerializer):
    """
    Serializer for the Contributor model. Detailed view of a
    Contributor.
    """
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'project',
            'time_created'
        ]


class ContributorSummarySerializer(ModelSerializer):
    """
    Serializer for the Contributor model. Minimal information, to
    display a list of the contributors name.
    """
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'user',
        ]


class ContributorCreateSerializer(ModelSerializer):
    """
    Serializer for the Contributor model. Serializer for creating a new
    Contributor.
    """
    class Meta:
        model = Contributor
        fields = [
            'user',
        ]


class ProjectListSerializer(ModelSerializer):
    """
    Serializer for the Project model. Minimal info + a link to the
    detailed view.
    """
    author = UserSummarySerializer(
        read_only=True
    )
    project_detail = HyperlinkedIdentityField(
        view_name='project-detail'
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'author',
            'project_detail',
        ]


class ProjectDetailSerializer(ModelSerializer):
    """
    Serializer for the Project model. Detailed view of a Project.
    It generates two links to the Project's Contributors endpoint and
    Project's Issues endpoint.
    """
    author = UserSummarySerializer(
        read_only=True
    )
    link_contributor = HyperlinkedIdentityField(
        view_name='project-contributor-list',
        lookup_url_kwarg='project_pk',
        read_only=True
    )
    contributors = ContributorSummarySerializer(
        many=True,
        read_only=True
    )
    link_issue = HyperlinkedIdentityField(
        view_name='project-issue-list',
        lookup_url_kwarg='project_pk',
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'author',
            'title',
            'description',
            'type',
            'time_created',
            'contributors',
            'link_contributor',
            'link_issue',
        ]


class ProjectCreateSerializer(ModelSerializer):
    """
    Serializer for the Project model. Serializer for creating a new
    Project.
    """
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'type',
        ]


class ProjectUpdateSerializer(ModelSerializer):
    """
    Serializer for the Project model. Serializer for updating a new
    Project.
    """
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'type',
        ]


class CommentListSerializer(ModelSerializer):
    """
    Serializer for the Comment model. Minimal info + a link to the
    detailed view.
    """
    author = UserSummarySerializer(
        read_only=True
    )
    comment_detail = NestedHyperlinkedIdentityField(
        view_name='issue-comment-detail',
        parent_lookup_kwargs={
            'project_pk': 'issue__project__pk', 'issue_pk': 'issue__pk'
        },
        lookup_field='id',
        lookup_url_kwarg='pk',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'comment_detail',
        ]


class CommentDetailSerializer(ModelSerializer):
    """
    Serializer for the Comment model. Detailed view of a Comment.
    """
    author = UserSummarySerializer(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'issue',
            'content',
            'time_created',
        ]


class CommentSummarySerializer(ModelSerializer):
    """
    Serializer for the Comment model. Minimal information, to be
    displayed in a list of comments.
    """
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'author'
        ]


class CommentCreateSerializer(ModelSerializer):
    """
    Serializer for the Comment model. Serializer for creating a new
    Comment.
    """
    class Meta:
        model = Comment
        fields = [
            'content',
        ]


class CommentUpdateSerializer(ModelSerializer):
    """
    Serializer for the Comment model. Serializer for updating a Comment.
    """
    class Meta:
        model = Comment
        fields = [
            'content'
        ]


class IssueListSerializer(ModelSerializer):
    """
    Serializer for the Issue model. Minimal info + a link to the
    detailed view.
    """
    author = UserSummarySerializer(
        read_only=True
    )
    issue_detail = NestedHyperlinkedIdentityField(
        view_name='project-issue-detail',
        parent_lookup_kwargs={'project_pk': 'project__pk'},
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'author',
            'project',
            'title',
            'issue_detail',
        ]


class IssueDetailSerializer(ModelSerializer):
    """
    Serializer for the Issue model. Detailed view of an issue.
    It generates a link to the Issue's Comments endpoint.
    """
    author = UserSummarySerializer(
        read_only=True
    )
    comments = CommentSummarySerializer(
        many=True,
        read_only=True
    )
    link_comment = NestedHyperlinkedIdentityField(
        view_name='issue-comment-list',
        parent_lookup_kwargs={'project_pk': 'project__pk'},
        lookup_field='pk',
        lookup_url_kwarg='issue_pk',
        read_only=True
    )
    assigned_to = UserSummarySerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'author',
            'project',
            'title',
            'description',
            'assigned_to',
            'priority',
            'type',
            'status',
            'time_created',
            'comments',
            'link_comment'
        ]


class IssueCreateSerializer(ModelSerializer):
    """
    Serializer for the Issue model. Serializer for creating a new issue.
    """
    assigned_to = PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        allow_null=True,
    )

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'assigned_to',
            'priority',
            'type',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        """
        Look for a project's contributors and give the list to the
        "assigned_to" field to limit the choices of designated users to
        the contributors of the project only.
        """
        super().__init__(*args, **kwargs)
        project_pk = self.context['view'].kwargs['project_pk']
        self.fields["assigned_to"].queryset = User.objects.filter(
            contributor__project_id=project_pk
        )


class IssueUpdateSerializer(ModelSerializer):
    """
    Serializer for the Issue model. Serializer for updating an issue.
    """
    assigned_to = PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        allow_null=True,
    )

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'assigned_to',
            'priority',
            'type',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        """
        Look for a project's contributors and give the list to the
        "assigned_to" field to limit the choices of designated users to
        the contributors of the project only.
        """
        super().__init__(*args, **kwargs)
        project_pk = self.context['view'].kwargs['project_pk']
        self.fields["assigned_to"].queryset = User.objects.filter(
            contributor__project_id=project_pk
        )
