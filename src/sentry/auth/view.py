from __future__ import absolute_import, print_function

__all__ = ('AuthView',)

from sentry.web.frontend.base import BaseView


class AuthView(BaseView):
    auth_required = False
    sudo_required = False

    def dispatch(self, request):
        raise NotImplementedError

    def get_next_url(self, request):
        return request.path

    def get_current_url(self, request):
        return request.path
