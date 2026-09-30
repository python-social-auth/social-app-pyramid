import unittest
from types import SimpleNamespace
from unittest.mock import patch

from social_pyramid.views import auth


class AuthViewTest(unittest.TestCase):
    @patch("social_pyramid.views.do_auth")
    def test_auth_passes_current_user_to_initiation_hook(self, do_auth) -> None:
        backend = object()
        user = object()
        request = SimpleNamespace(backend=backend, user=user)
        expected = object()
        do_auth.return_value = expected

        response = auth.__wrapped__(request)

        self.assertIs(response, expected)
        do_auth.assert_called_once_with(backend, redirect_name="next", user=user)
