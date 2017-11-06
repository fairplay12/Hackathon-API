from functools import wraps


def login_required(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if method_args[0].context.user.is_authenticated:
            return method(self, *method_args, **method_kwargs)
        else:
            return method_args[0].context.error

    return _impl
