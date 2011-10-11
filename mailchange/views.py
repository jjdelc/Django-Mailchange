# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from mailchange import strings
from mailchange.models import MailChange
from mailchange.forms import MailChangeForm, MailChangeConfirmationForm

@login_required
def change_mail(request):
    """
    On GET:
        Displays a form to change the user's email address
    On POST:
        Perform mail change, create a new MailChange model for the user
    """
    form = MailChangeForm()
    if request.method == 'POST':
        form = MailChangeForm(request.POST)
        if form.is_valid():
            mail_change = form.save_and_notify(request.user)
            return HttpResponseRedirect(reverse('change_request_sent'))
    
    return direct_to_template(request, 'mailchange/change_form.html', {
        'form': form,
    })


@login_required
def change_request_sent(request):
    """
    Displays a confirmation page with instructions on how to follow the 
    change mail process
    """
    return direct_to_template(request, 'mailchange/change_request_sent.html')


def confirm(request, uuid):
    """
    This is the endpoint where the user confirms the mail switch.
    This page shows a form to enter the current user's password to confirm
    """

    change_request = get_object_or_404(MailChange, uuid=uuid)
    form = MailChangeConfirmationForm(change_request.user)
    if request.method == 'POST':
        form = MailChangeConfirmationForm(change_request.user, request.POST)
        if form.is_valid():
            change_request.change_mail()
            messages.info(request, strings.MAIL_CHANGED)
            return HttpResponseRedirect(reverse('user_profile'))

    return direct_to_template(request, 'mailchange/confirm_change.html',  {
        'form': form,
        'change_request': change_request,
        'uuid': uuid,
    })

