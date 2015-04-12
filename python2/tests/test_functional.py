import unittest
import sys, logging, socket, os
from raygun4py import raygunprovider

class TestRaygun4PyFunctional(unittest.TestCase):

    def setUp(self):
        self.apiKey = "kImNMh/h98JZ233PUKv87g=="

    def test_track_with_user(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_user({
            'firstName': 'foo',
            'fullName': 'foo bar',
            'email': 'foo@bar.com',
            'isAnonymous': False,
            'identifier': 'foo@bar.com'
          })

        try:
            raise Exception("Raygun4py manual sending test - user")
        except:
            httpResult = client.track_exception(sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def test_track_with_version(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_version('v1.0.0')

        try:
            raise Exception("Raygun4py manual sending test - user")
        except:
            httpResult = client.track_exception(sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def log_send(self, logger):
        try:
            raise StandardError("Raygun4py Logging Test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error("Logging with sending", exc_info = (exc_type, exc_value, exc_traceback))
            return 0

        return 1

    def log_nosend(self, logger):
        try:
            raise StandardError("Raygun4py Logging Test")
        except:
            logger.error("Logging without sending")
            return 0

        return 1

    def test_log_with_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEquals(0, self.log_send(logger))


    def test_log_without_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEquals(0, self.log_nosend(logger))

    def test_track_exception_no_args(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception")
        except:
            httpResult = client.track_exception()

            self.assertEqual(httpResult[0], 202)

    def test_track_exception_with_exc_info(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise StandardError("Raygun4py manual sending test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            httpResult = client.track_exception(sys.exc_info())


    def test_send_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception")
        except Exception as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult[0], 202)

    def test_send_exception_with_exc_info(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception with exc_info")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def test_send_exception_subclass(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise CustomException("Raygun4py functional test - Py2 send_exception with custom exception")
        except CustomException as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult[0], 202)

    def test_ignore_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.ignore_exceptions(['CustomException'])

        try:
            raise CustomException("This test should not send an exception")
        except CustomException as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult, None)

    def test_filter_keys_202(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.filter_keys(['environment'])

        try:
            raise Exception("Raygun4py functional test - Py2 filter_keys")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())
        
        self.assertEqual(httpResult[0], 202)

    @unittest.skip('Requires a proxy, skipping for Travis')
    def test_proxy(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_proxy('127.0.0.1', 3128)

        try:
            raise Exception("Raygun4py functional test - Py2 set_proxy")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())
        
        self.assertEqual(httpResult[0], 202)


class CustomException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)