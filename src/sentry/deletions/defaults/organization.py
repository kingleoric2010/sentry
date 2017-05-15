from __future__ import absolute_import, print_function

from ..base import DeletionTask, Relation


class OrganizationDeletionTask(DeletionTask):
    def get_child_relations(self, instance):
        from sentry.models import (
            OrganizationMember,
            Commit, CommitAuthor, CommitFileChange, Environment, Release, ReleaseCommit,
            ReleaseEnvironment, ReleaseFile, Distribution, ReleaseHeadCommit, Repository,
            Team
        )

        # Team must come first
        relations = [
            Relation(Team, {'organization_id': instance.id}),
        ]

        model_list = (
            OrganizationMember, CommitFileChange, Commit, CommitAuthor,
            Environment, Repository, Release, ReleaseCommit,
            ReleaseEnvironment, ReleaseFile, Distribution, ReleaseHeadCommit
        )
        relations.extend([
            Relation(m, {'organization_id': instance.id}) for m in model_list
        ])

        return relations
