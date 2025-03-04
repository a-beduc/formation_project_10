from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, HyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from myauth.serializers import UserListSerializer, UserSummarySerializer
from softdesk.models import Project, Issue, Contributor, Comment


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


class ContributorSummarySerializer(ModelSerializer):
    user = UserSummarySerializer(read_only=True)

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
