from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from datetime import datetime

class UIForm(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('uiform_detail', (), {'pk': self.id})

    @models.permalink
    def get_public_url(self):
        return ('uiform_detail_public', (), {'pk': self.id})

    def fields(self):
        return self.uiformfield_set.all()

    def as_a(self):
        return mark_safe('<a href="%s">%s</a>' % (self.get_absolute_url(), self.name))

class UIFormField(models.Model):
    FIELD_TYPE_CHOICES = (
        ('b', 'Boolean'),
        ('i', 'Integer'),
        )
    field_type = models.CharField(max_length=1, choices=FIELD_TYPE_CHOICES)
    created_at = models.DateTimeField(default=datetime.now())
    label = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    ui_form = models.ForeignKey(UIForm)

    def __unicode__(self):
        return self.label

    def as_html(self):
        if self.field_type == 'b':
            input_type = 'checkbox'
        elif self.field_type == 'i':
            input_type = 'text'
        return mark_safe('<label for="uiformfield-%s">%s</label><input type="%s" id="uiformfield-%s"/><p class="formHint">%s</p>' %
                         (self.id, self.label, input_type, self.id, self.description))
