from __future__ import absolute_import, print_function

__all__ = ['DeletionTaskManager']


class DeletionTaskManager(object):
    def __init__(self, default_task=None):
        self.tasks = {}
        self.default_task = default_task

    def get(self, model, query, **kwargs):
        try:
            task = self.tasks[model]
        except KeyError:
            task = self.default_task
        return task(
            manager=self,
            model=model,
            query=query,
            **kwargs
        )

    def register(self, model, task):
        self.tasks[model] = task
