from __future__ import absolute_import, print_function


class Implementation(object):
    def __init__(self, **config):
        self.config = config

    def get_config_form(self, request):
        # return FormClass(request.POST or Nont)
        raise NotImplementedError

    def get_auth_pipeline(self):
        # return []
        raise NotImplementedError
