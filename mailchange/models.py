# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django_extensions.db.fields import UUIDField, CreationDateTimeField
try:
   from mailer import send_mail
except ImportError:
   from django.core.mail import send_mail

from mailchange import strings, settings

def first_line(text):
    """
    Returns the first line from a chunk of trext
    """
    return text.split('\n')[0]

class MailChange(models.Model):
    user = models.ForeignKey(User)
    uuid = UUIDField()
    email = models.EmailField()
    created_on = CreationDateTimeField()

    class Meta:
        ordering = ('-created_on',)
        verbose_name = strings.MAIL_CHANGE
        verbose_name_plural = strings.MAIL_CHANGE_PLURAL

    def __unicode__(self):
        return strings.MAIL_CHANGE_STR % (self.email, self.user)

    def change_mail(self):
        """
        Sets the user's mail to the new one and deletes this registry
        """
        user = self.user
        user.email = self.email
        user.save()
        if settings.NOTIFY_NEW_ADDRESS:
            self.notify_to_new_address()
        self.delete()

    def build_mail_ctx(self):
        site = Site.objects.get_current()
        return {
            'site': site,
            'mail_change': self,
        }

    def notify_to_new_address(self):
        """
        Sends a notification to the *NEW* email address about the
        mail change
        """
        ctx = self.build_mail_ctx()
        subject = first_line(render_to_string(
            'mailchange/notification_subject.txt',
            ctx))
        body = render_to_string('mailchange/notification_body.txt', ctx)
        send_mail(subject, body, settings.CHANGE_MAIL_FROM, [self.email])
        
    def send_confirmation_mail(self):
        """
        Sends a confirmation mail to the *CURRENT* email address with 
        instructions
        """
        ctx = self.build_mail_ctx()
        subject = first_line(render_to_string(
            'mailchange/confirmation_subject.txt',
            ctx))
        body = render_to_string('mailchange/confirmation_body.txt', ctx)
        send_mail(subject, body, settings.CHANGE_MAIL_FROM, [self.user.email])

    @models.permalink
    def get_confirmation_url(self):
        return ('change_mail_confirm', (), {
            'uuid': self.uuid
        })

