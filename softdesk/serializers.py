from rest_framework.serializers import ModelSerializer
from softdesk.models import Project, Issue, Contributor, Comment


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'project',
            'time_created'
        ]


class ProjectSerializer(ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'author',
            'title',
            'description',
            'type',
            'time_created',
            'contributors'
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'issue',
            'description',
            'time_created'
        ]


class IssueSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

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
            'comments'
        ]
