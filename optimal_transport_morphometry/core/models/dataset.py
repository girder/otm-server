from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from guardian.shortcuts import get_objects_for_user
from s3_file_field import S3FileField


class Dataset(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(default='', blank=True, max_length=3000)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name='datasets_owned', on_delete=models.CASCADE)

    class ProcessStatus(models.TextChoices):
        PENDING = 'Pending'
        RUNNING = 'Running'
        FINISHED = 'Finished'
        FAILED = 'Failed'

    # Preprocessing
    current_preprocessing_batch = models.OneToOneField(
        'PreprocessingBatch', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )

    # Analysis
    analysis_result = S3FileField(null=True, blank=True)
    analysis_status = models.CharField(
        max_length=32, choices=ProcessStatus.choices, default=ProcessStatus.PENDING
    )

    class Meta:
        permissions = (('collaborator', 'Collaborator'),)
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_owner_dataset_name')
        ]

    def user_access(self, user: User):
        # Must check this before passing to user.has_perm
        if not user.is_authenticated:
            return None

        if user.id == self.owner_id:
            return 'owner'

        if user.has_perm('collaborator', self):
            return 'collaborator'

        return None

    @staticmethod
    def visible_datasets(user: User) -> models.QuerySet[Dataset]:
        # Handle unauthenticated user
        if not user.is_authenticated:
            return Dataset.objects.filter(public=True)

        # Construct queryset for all shared datasets
        shared_pks = get_objects_for_user(
            user, 'collaborator', Dataset, with_superuser=False
        ).values_list('id', flat=True)

        # Return all public, shared and owned datasets
        return Dataset.objects.filter(
            models.Q(public=True) | models.Q(owner_id=user.id) | models.Q(pk__in=shared_pks)
        )
