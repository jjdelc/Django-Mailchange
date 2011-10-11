# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
try:
   from mailer import send_mail
except ImportError:
   from django.core.mail import send_mail

from mailchange import strings
from mailchange.models import MailChange

class MailChangeForm(forms.ModelForm):
    class Meta:
        model = MailChange
        exclude = ('user', 'uuid', 'created_on')

    def __init__(self, *args, **kwargs):
        super(MailChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = strings.NEW_MAIL_LABEL

    def clean_email(self):
        """
        The email address must be unique
        """
        data = self.cleaned_data
        try:
            User.objects.get(email=data['email'])
            raise forms.ValidationError(strings.DUPLICATE_EMAIL)
        except User.DoesNotExist:
            return data['email']

    def save_and_notify(self, user):
        """
        Creates the new mailchange object and sends a notification to the new
        email
        """
        mail_change = super(MailChangeForm, self).save(commit=False)
        mail_change.user = user
        mail_change.save()
        mail_change.send_confirmation_mail()


class MailChangeConfirmationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super(MailChangeConfirmationForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        data = self.cleaned_data
        password = data['password']
        if self.user.check_password(password):
            return password

        raise forms.ValidationError(strings.INCORRECT_PASSWORD)

