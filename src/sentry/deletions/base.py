from __future__ import absolute_import, print_function

import logging


class Relation(object):
    def __init__(self, model, query_cb, task=None):
        self.model = model
        self.query_cb = query_cb
        self.task = task


class DeletionTask(object):
    logger = logging.getLogger('sentry.deletions.async')

    def __init__(self, manager, model, query, transaction_id=None,
                 actor=None, chunk_size=100):
        self.manager = manager
        self.model = model
        self.query = query
        self.transaction_id = transaction_id
        self.actor = actor
        self.chunk_size = chunk_size

    def chunk(self):
        """
        Deletes a chunk of this instance's data. Return ``True`` if there is
        more work, or ``False`` if the entity has been removed.
        """
        queryset = list(self.model.objects.filter(
            **self.query
        )[:self.chunk_size + 1])
        has_more = self.delete_bulk(self, queryset[:self.chunk_size])
        if has_more:
            return has_more
        return len(queryset) > self.chunk_size

    def get_child_relations(self, instance):
        # TODO(dcramer): it'd be nice if we collected the default relationships
        return [
            # Relation(Model, {'parent_id': instance.id})
        ]

    def delete_bulk(self, instance_list):
        for instance in instance_list:
            child_relations = self.get_child_relations(instance)
            if child_relations:
                has_more = self.delete_children(instance, child_relations)
                if has_more:
                    return has_more
        return self.delete_instance(instance)

    def delete_instance(self, instance):
        instance_id = instance.id
        instance.delete()
        self.logger.info('object.delete.executed', extra={
            'object_id': instance_id,
            'transaction_id': self.transaction_id,
            'app_label': instance._meta.app_label,
            'model': type(instance).__name__,
        })
        return False

    def delete_children(self, instance, relations):
        # Ideally this runs through the deletion manager
        has_more = False
        for relation in relations:
            task = self.manager.get(
                model=relation.model,
                query=relation.query,
                transaction_id=self.transaction_id,
                actor=self.actor,
                chunk_size=self.chunk_size,
            )
            has_more = task.chunk()
            if has_more:
                return has_more
        return has_more
