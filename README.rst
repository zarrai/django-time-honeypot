===============
django-honeypot with time restriction
===============


Based on this repository: https://github.com/jamesturk/django-honeypot/

Usage
=====

settings.py
-----------

Be sure to add ``honeypot`` to ``INSTALLED_APPS`` and ``honeypot.middleware.HoneypotMiddleware`` to ``MIDDLEWARE`` in settings.py.

You will almost always need to define ``HONEYPOT_FIELD_NAME`` which is the name to use for the honeypot field.  Some sophisticated bots will attempt to avoid fields named honeypot, so it may be wise to name the field something slightly more realistic such as "phonenumber" or "body2".

``HONEYPOT_VALUE`` is an option that you can specify to populate the honeypot field, by default the honeypot field will be empty and any text entered into it will result in a failed POST.  ``HONEYPOT_VALUE`` can be a string or a callable that takes no arguments.



Adding honeypot fields site-wide
--------------------------------

This is particularly useful when dealing with apps that render their own forms.  For this purpose three middlewares are provided, similar in functionality to django's own CSRF middleware.

All of these middleware live in ``honeypot.middleware``.

``HoneypotResponseMiddleware`` analyzes the output of all responses and rewrites any forms that use ``method="POST"`` to contain a honeypot field, just as if they had started with ``{% render_honeypot_field %}``.  Borrowing heavily from ``django.contrib.csrf.middleware.CsrfResponseMiddleware`` this middleware only rewrites responses with Content-Type text/html or application/xhtml+xml.

``HoneypotViewMiddleware`` ensures that for all incoming POST requests to views ``request.POST`` contains a valid honeypot field as defined by the ``HONEYPOT_FIELD_NAME``, ``HONEYPOT_VALUE``, and ``HONEYPOT_VERIFIER`` settings.  The result is the same as if every view in your project were decorated with ``@check_honeypot``.

``HoneypotMiddleware`` is a combined middleware that applies both ``HoneypotResponseMiddleware`` and ``HoneypotViewMiddleware``, this is the easiest way to get honeypot fields site-wide and can be used in many if not most cases.

Adding time restriction
-----------------------
Add ``MIN_DURATION`` and ``MAX_DURATION`` to settings.py by default min_duration value is 2 seconds and the max_duration is 3 hours .

Customizing honeypot display
----------------------------

There are two templates used by django-honeypot that can be used to control various aspects of how the honeypot functionality is presented to the user.

``honeypot/honeypot_field.html`` is used to render the honeypot field.  It is given two context variables ``fieldname`` and ``value``, corresponding to ``HONEYPOT_FIELD_NAME`` and ``HONEYPOT_VALUE`` or any overrides in effect (such as a custom field name passed to the template tag).

``honeypot/honeypot_error.html`` is the error page rendered when a bad request is intercepted.  It is given the context variable ``fieldname`` representing the name of the honeypot field.

