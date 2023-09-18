from __future__ import absolute_import
import datetime

import six

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AbstractBase(models.Model):
    """
    Abstract model for all base models of different databases.
    """

    timestamp = models.DateTimeField(blank=True, db_index=True)
    hidden = models.BooleanField(default=False, db_index=True)
    trashed = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        if hasattr(self, "__unicode__"):
            return self.__unicode__()

        return super(AbstractBase, self).__str__()

    class Meta:
        abstract = True

    # Override save method.
    def save(self, *args, **kwargs):  # pylint: disable=W0221
        if not self.timestamp:
            self.timestamp = datetime.datetime.now()
        update_timestamp = kwargs.pop("update_timestamp", False)
        if update_timestamp:
            self.timestamp = datetime.datetime.now()

        # XXX: Remove this once you have verified that kwargs never contains
        # update key.
        kwargs.pop("update", False)

        super(AbstractBase, self).save(*args, **kwargs)

    # Override delete method.
    def delete(self, **kwargs):  # pylint: disable=W0221
        super(AbstractBase, self).delete(**kwargs)

    # Define hide method.
    def hide(self, **kwargs):
        model = self.__class__
        kwargs.update({"hidden": True})
        model.objects.using(self._db).filter(pk=self.id).update(**kwargs)

    def _available(self):
        return not self.hidden and not self.trashed

    available = property(_available)

    def update(self, **kwargs):
        """
        Update method on an instance which is thread safe and avoids
        deadlocks. You shouldn't call save() if you are updating an instance.
        """

        if self.id is None:
            raise ValueError("Update called on an unsaved instance!")

        use_raw_update = kwargs.pop("use_raw_update", False)

        # Call update instead of save.
        if use_raw_update:
            self.__update_using_raw_sql(**kwargs)
        else:
            self.__class__.objects.filter(pk=self.id).update(**kwargs)

        # Populate object with kwargs.
        for name, value in six.iteritems(kwargs):
            setattr(self, name, value)

        return self


class Base(AbstractBase):
    """
    Abstract model for master database models.
    """

    def __init__(self, *args, **kwargs):
        self._db = "default"
        super(Base, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def get_content_type(self):
        try:
            if hasattr(ContentType, "objects_cache"):
                return ContentType.objects_cache.get_for_model(self)
        except Exception:
            pass
        return ContentType.objects.get_for_model(self)

    @classmethod
    def cls_content_type(cls):
        try:
            if hasattr(ContentType, "objects_cache"):
                return ContentType.objects_cache.get_for_model(cls)
        except Exception:
            pass
        return ContentType.objects.get_for_model(cls)


class Ownable(models.Model):
    """
    Abstract model that provides ownership of an object for a user.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Author", db_index=True
    )

    class Meta:
        abstract = True

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.user_id


class Generic(models.Model):
    """
    Abstract model for generic content types.
    """

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, db_index=True, null=True
    )
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
