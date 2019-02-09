from __future__ import absolute_import, unicode_literals
import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Load celery when docker is up! check Dockerfile
if os.environ.get('DOCKERUP'):
    from .celery import app as celery_app
    __all__ = ('celery_app',)
