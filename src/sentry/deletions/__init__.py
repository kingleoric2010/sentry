from __future__ import absolute_import

from .base import DeletionTask
from .manager import DeletionTaskManager

default_manager = DeletionTaskManager(default_task=DeletionTask)


def load_defaults():
    from sentry.models import Organization, Project
    from . import defaults

    default_manager.register(Organization, defaults.OrganizationDeletionTask)
    default_manager.register(Project, defaults.ProjectDeletionTask)


load_defaults()

get = default_manager.get
register = default_manager.register
