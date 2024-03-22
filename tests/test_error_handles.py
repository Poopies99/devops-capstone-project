import os
import logging
from unittest import TestCase
from service import talisman
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app

BASE_URL = "/accounts"

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


class TestErrorHandlers(TestCase):
    """Error Handlers Tests"""
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)
        talisman.force_https = False

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    def test_bad_request_error(self):
        """It should return a 400 error for bad requests"""
        response = self.client.post(BASE_URL, data="not a valid json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("Bad Request", data["error"])

    def test_not_found_error(self):
        """It should return a 404 error for missing resources"""
        response = self.client.get(f"{BASE_URL}/9999")  # Assuming 9999 is an ID that does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("Not Found", data["error"])

    def test_method_not_supported_error(self):
        """It should return a 405 error for unsupported methods"""
        response = self.client.put(BASE_URL)  # Assuming PUT is not supported on the base URL
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.get_json()
        self.assertIn("Method not Allowed", data["error"])

    def test_mediatype_not_supported_error(self):
        """It should return a 415 error for unsupported media types"""
        response = self.client.post(BASE_URL, data="{}", content_type="application/xml")  # Assuming XML is not supported
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = response.get_json()
        self.assertIn("Unsupported media type", data["error"])

    def test_internal_server_error(self):
        """It should return a 500 error for internal server errors"""
        # To trigger an internal server error, you might need to mock or simulate a failure
        # For example, mocking a database service to throw an exception
        # This is highly specific to your application's architecture and error handling logic

        # Here's a hypothetical example if there was a route that could raise an unexpected error:
        # with mock.patch('service.routes.some_internal_function', side_effect=Exception('Internal server error')):
        #     response = self.client.get('/some-route-that-causes-error')
        #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        #     data = response.get_json()
        #     self.assertIn("Internal Server Error", data["error"])
        pass  # Replace or remove this with actual implementation based on your application logic

