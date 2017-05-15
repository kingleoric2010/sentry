from __future__ import absolute_import, print_function

from ..base import DeletionTask, Relation


class TeamDeletionTask(DeletionTask):
    def get_child_relations(self, instance):
        from sentry.models import Project

        return [
            Relation(Project, {'organization_id': instance.id}),
        ]
