import os

import unittest

from flask import current_app as app
from flask_testing import TestCase

from app.main.config import basedir

class TestAuthorizationRessource(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_get_authorization_url(self):
        response = self.client.get('localhost:5000/authorize')
        self.assert200(response, message='/authorize test failed.')
    