import os
from time import time

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


def validate_image(fieldfile_obj):
            filesize = fieldfile_obj.file.size
            megabyte_limit = 4.0
            if filesize > megabyte_limit*1024*1024:
                raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

def get_upload_file_name(instance, filename):
    return "upload_files/{0}_{1}" .format(
        str(time()).replace('.', '_'),
        filename
    )


class BaseInfo(models.Model):
    """Base class containing all models common information."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Define Model as abstract."""

        abstract = True


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]


class CakeDisplay(BaseInfo):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    description = models.TextField(
        max_length=280, default="Cake Creativity...")
    image = models.ImageField(
        upload_to=get_upload_file_name, 
        validators=[validate_image], 
        blank=True, 
        help_text='Maximum file size allowed is 2Mb'
    )

    def __str__(self):
        return "{} with price N{}" .format(self.name, self.price)

    class Meta:
        ordering = ('-created_at',)


@receiver(post_delete, sender=CakeDisplay)
def delete_from_file_system(sender, instance, **kwargs):

    path = instance.image.path

    filepath, ext = os.path.splitext(path)
    delete_path = filepath + 'edited' + ext

    if os.path.exists(delete_path):
        os.remove(delete_path)
    if os.path.exists(path):
        os.remove(path)
