from functools import wraps
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
import datetime    
    
    
def honeypot_verifier(val):
    """
        HONEYPOT_VERIFIER function
        Ensures that filling the forms takes a minimum amount of time and checks the field value is datetime.
    """
    try:
        delivery = datetime.datetime.strptime(val,"%Y-%m-%d %H:%M:%S")
    except:
        return False
    now = datetime.datetime.now()
    duration = now - delivery
    min_duration = datetime.timedelta(seconds= getattr(settings, 'MIN_DURATION', 2))
    max_duration = datetime.timedelta(seconds= getattr(settings, 'MAX_DURATION', 3600))
    if duration < min_duration or duration > max_duration:
        return False
    return True


def verify_honeypot_value(request, field_name):
    """
        Verify that request.POST[field_name] is a valid honeypot.

        Ensures that the field exists and passes verification according to
        HONEYPOT_VERIFIER.
    """
    verifier = honeypot_verifier
    if request.method == 'POST':
        field = getattr(settings, 'HONEYPOT_FIELD_NAME', field_name)
        if field not in request.POST or not verifier(request.POST[field]):
            return render(
                request,
                'honeypot/honeypot_error.html',
                {'fieldname': field},
                None,
                400
            )


def check_honeypot(func=None, field_name=None):
    """
        Check request.POST for valid honeypot field.

        Takes an optional field_name that defaults to HONEYPOT_FIELD_NAME if
        not specified.
    """
    # hack to reverse arguments if called with str param
    if isinstance(func, str):
        func, field_name = field_name, func

    def decorated(func):
        def inner(request, *args, **kwargs):
            response = verify_honeypot_value(request, field_name)
            if response:
                return response
            else:
                return func(request, *args, **kwargs)
        return wraps(func)(inner)

    if func is None:
        def decorator(func):
            return decorated(func)
        return decorator
    return decorated(func)


def honeypot_exempt(view_func):
    """
        Mark view as exempt from honeypot validation
    """
    # borrowing liberally from django's csrf_exempt
    def wrapped(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped.honeypot_exempt = True
    return wraps(view_func)(wrapped)
