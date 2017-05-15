from __future__ import absolute_import, print_function

from ..base import DeletionTask, Relation


class ProjectDeletionTask(DeletionTask):
    def get_child_relations(self, instance):
        from sentry.models import (
            Activity, Event, EventMapping, EventUser, Group, GroupAssignee,
            GroupBookmark,
            GroupEmailThread, GroupHash, GroupMeta, GroupRelease, GroupResolution,
            GroupRuleStatus, GroupSeen, GroupSubscription, GroupSnooze, GroupTagKey,
            GroupTagValue, ProjectBookmark, ProjectKey,
            ReleaseProject, SavedSearchUserDefault, SavedSearch,
            TagKey, TagValue, UserReport, EnvironmentProject
        )

        relations = [
            # ProjectKey gets revoked immediately, in bulk
            Relation(ProjectKey, {'project_id': instance.id})
        ]

        # in bulk
        model_list = (
            Activity, EventMapping, EventUser, GroupAssignee, GroupBookmark,
            GroupEmailThread, GroupHash, GroupRelease, GroupRuleStatus, GroupSeen,
            GroupSubscription, GroupTagKey, GroupTagValue, ProjectBookmark,
            ProjectKey, TagKey, TagValue, SavedSearchUserDefault, SavedSearch,
            UserReport, EnvironmentProject
        )
        relations.extend([
            Relation(m, {'project_id': instance.id}) for m in model_list
        ])

        model_list = (GroupMeta, GroupResolution, GroupSnooze)
        relations.extend([
            Relation(m, {'project_id': instance.id}) for m in model_list
        ])

        # special case event due to nodestore
        relations.extend([
            Relation(Event, {'project_id': instance.id})
        ])

        # in bulk
        # Release needs to handle deletes after Group is cleaned up as the foreign
        # key is protected
        model_list = (Group, ReleaseProject)
        relations.extend([
            Relation(m, {'project_id': instance.id}) for m in model_list
        ])

        return relations
