from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from myauth.serializers import UserListSerializer, UserSummarySerializer
from softdesk.models import Project, Issue, Contributor, Comment
from myauth.models import User


class ContributorListSerializer(ModelSerializer):
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
            'project',
            'contributor_detail',
        ]


class ContributorDetailSerializer(ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'project',
            'time_created'
        ]


class ContributorSummarySerializer(ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'user',
        ]


class ContributorCreateSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = [
            'user',
        ]


class ProjectListSerializer(ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    project_detail = HyperlinkedIdentityField(view_name='project-detail', lookup_field='pk')

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'author',
            'project_detail',
        ]


class ProjectDetailSerializer(ModelSerializer):
    author = UserListSerializer(read_only=True)
    link_contributor = HyperlinkedIdentityField(
        view_name='project-contributor-list',
        lookup_field='pk',
        lookup_url_kwarg='project_pk',
        read_only=True
    )
    contributors = ContributorSummarySerializer(many=True, read_only=True)
    link_issue = HyperlinkedIdentityField(
        view_name='project-issue-list',
        lookup_field='pk',
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
    # Enlever author de la liste quand on met les perms self.request = author

    class Meta:
        model = Project
        fields = [
            'author',
            'title',
            'description',
            'type',
        ]


class ProjectUpdateSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'author',
            'title',
            'description',
            'type',
        ]


class CommentListSerializer(ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    comment_detail = NestedHyperlinkedIdentityField(
        view_name='issue-comment-detail',
        parent_lookup_kwargs={'project_pk': 'issue__project__pk', 'issue_pk': 'issue__pk'},
        lookup_field='id',
        lookup_url_kwarg='pk',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'description',
            'comment_detail',
        ]


class CommentDetailSerializer(ModelSerializer):
    author = UserListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'issue',
            'description',
            'time_created',
        ]


class CommentSummarySerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
        ]


class CommentCreateSerializer(ModelSerializer):
    # author à retirer car comment = request.user

    class Meta:
        model = Comment
        fields = [
            'author',
            'description',
        ]


class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description'
        ]


class IssueListSerializer(ModelSerializer):
    author = UserSummarySerializer(read_only=True)
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
    author = UserListSerializer(read_only=True)
    comments = CommentSummarySerializer(many=True, read_only=True)
    link_comment = NestedHyperlinkedIdentityField(
        view_name='issue-comment-list',
        parent_lookup_kwargs={'project_pk': 'project__pk'},
        lookup_field='pk',
        lookup_url_kwarg='issue_pk',
        read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'author',
            'project',
            'title',
            'description',
            'to_user',
            'priority',
            'type',
            'status',
            'time_created',
            'comments',
            'link_comment'
        ]


class IssueCreateSerializer(ModelSerializer):
    # enlever author de la liste quand on aura les perms sur qui accède à cette ressource car author = request.user

    class Meta:
        model = Issue
        fields = [
            'author',
            'title',
            'description',
            'to_user',
            'priority',
            'type',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_pk = self.context['view'].kwargs['project_pk']
        self.fields["to_user"].queryset = User.objects.filter(
            contributor__project_id=project_pk
        )

    # seems like it's not working and not used bc
    # def validate_to_user(self, value):
    #     project_pk = self.context['view'].kwargs['project_pk']
    #     is_contributor = Contributor.objects.filter(
    #         project_id=project_pk, user_id=value.pk
    #     ).exists()
    #     if not is_contributor:
    #         raise ValidationError('User is not a contributor')
    #     return value


class IssueUpdateSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'to_user',
            'priority',
            'type',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_pk = self.context['view'].kwargs['project_pk']
        self.fields["to_user"].queryset = User.objects.filter(
            contributor__project_id=project_pk
        )

    # seems like it's not working and not useful
    # def validate_to_user(self, value):
    #     project_pk = self.context['view'].kwargs['project_pk']
    #     is_contributor = Contributor.objects.filter(
    #         project_id=project_pk, user_id=value.pk
    #     ).exists()
    #     if not is_contributor:
    #         raise ValidationError('User is not a contributor')
    #     return value
