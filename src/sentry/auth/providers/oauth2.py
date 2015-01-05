from __future__ import absolute_import, print_function

from urllib import urlencode
from uuid import uuid4

from sentry.auth import Implementation, AuthView
from sentry.http import safe_urlopen, safe_urlread
from sentry.utils import json
from sentry.utils.http import absolute_uri


class OAuth2Login(AuthView):
    def __init__(self, authorize_url, client_id, *args, **kwargs):
        super(OAuth2Login, self).__init__(*args, **kwargs)
        self.authorize_url = authorize_url
        self.client_id = client_id

    def get_authorize_url(self):
        return self.authorize_url

    def get_authorize_params(self, state, redirect_uri):
        return {
            "client_id": self.client_id,
            "response_type": "code",
            "duration": "temporary",
            "scope": "identity",
            "state": state,
            "redirect_uri": redirect_uri,
        }

    def dispatch(self, request):
        state = str(uuid4())

        params = self.get_authorized_params(
            state=state,
            redirect_uri=absolute_uri(self.get_next_url(request)),
        )

        redirect_uri = self.get_authorize_url() + '?' + urlencode(params)

        self.bind_session(request, 'state', state)

        return self.redirect(redirect_uri)


class OAuth2Callback(AuthView):
    def __init__(self, access_token_uri, *args, **kwargs):
        super(OAuth2Login, self).__init__(*args, **kwargs)
        self.access_token_uri = access_token_uri

    def get_token_params(self, code, redirect_uri):
        return {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

    def exchange_token(self, request, code):
        # TODO: this needs the auth yet
        params = self.get_token_params(
            code=code,
            redirect_uri=absolute_uri(self.get_current_url(request)),
        )
        req = safe_urlopen(self.access_token_uri, data=params)
        resp = safe_urlread(req)

        return json.loads(resp)

    def dispatch(self, request):
        error = request.GET.get('error')
        state = request.GET.get('state')
        code = request.GET.get('code')

        if error:
            raise NotImplementedError

        if state != self.fetch_session(request, 'state'):
            raise NotImplementedError

        data = self.exchange_token(request, code)

        self.bind_session(request, 'data', data)

        return self.redirect(self.get_next_url())


class OAuth2Implementation(Implementation):
    def get_auth_pipeline(self):
        return [OAuth2Login(), OAuth2Callback()]
