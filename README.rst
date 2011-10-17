=================
Django Mailchange
=================

Plug and play app to allow your users to change their email addresses via
verification email.


How it works
------------

This app will save the mail change requests in a temporary model instead of 
changing the user's email address immediatly in favor of doing it after the
new email address has been verified.

A confirmation email will be sent to the new email address with a link. The 
confirmation page will ask the user to enter her password to verify she's the 
account owner and then proceed with the mail changing.

Installation
------------

 * Add 'mailchange' to your INSTALLED APPS
 * Syncdb
 * Include 'mailchange.urls' somewhere in you url patterns

====
TODO
====

* Write tests
* Write docs
