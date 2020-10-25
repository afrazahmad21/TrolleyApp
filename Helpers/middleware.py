from functools import wraps

from flask import session, render_template


def protected_route():
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if not session['email']:
                return render_template('Login.html', error="Login required")
            return func(*args, **kwargs)

        return authorize

    return decorator
