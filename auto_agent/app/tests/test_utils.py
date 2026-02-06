import base64
import json
import os
import sys
import time
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import all utility modules
try:
    from app.utils.base64_utils import Base64Utils
except ImportError:
    Base64Utils = None

try:
    from app.utils.crypto_utils import CryptoUtils
except ImportError:
    CryptoUtils = None

try:
    from app.utils.email_utils import EmailUtils
except ImportError:
    EmailUtils = None

try:
    from app.utils.file_utils import FileUtils
except ImportError:
    FileUtils = None

try:
    from app.utils.http_utils import HttpUtils
except ImportError:
    HttpUtils = None

try:
    from app.utils.json_utils import JsonUtils
except ImportError:
    JsonUtils = None

try:
    from app.utils.logger import Logger
except ImportError:
    Logger = None

try:
    from app.utils.random_utils import RandomUtils
except ImportError:
    RandomUtils = None

try:
    from app.utils.string_utils import StringUtils
except ImportError:
    StringUtils = None

try:
    from app.utils.time_utils import TimeUtils
except ImportError:
    TimeUtils = None


class TestBase64Utils(unittest.TestCase):
    """Test base64 utils module"""

    if Base64Utils:

        def test_base64_encode(self):
            """Test Base64Utils.encode method"""
            test_string = "Hello, World!"
            encoded = Base64Utils.encode(test_string)
            self.assertIsInstance(encoded, str)
            # Verify decoding gives back original
            decoded = base64.b64decode(encoded).decode("utf-8")
            self.assertEqual(decoded, test_string)

        def test_base64_decode(self):
            """Test Base64Utils.decode method"""
            test_string = "Hello, World!"
            encoded = base64.b64encode(test_string.encode("utf-8")).decode("utf-8")
            decoded = Base64Utils.decode(encoded)
            self.assertIsInstance(decoded, str)
            self.assertEqual(decoded, test_string)


class TestCryptoUtils(unittest.TestCase):
    """Test crypto utils module"""

    if CryptoUtils:

        def test_crypto_hash(self):
            """Test CryptoUtils.hash method"""
            test_string = "Hello, World!"
            hashed = CryptoUtils.hash(test_string)
            self.assertIsInstance(hashed, str)
            self.assertTrue(len(hashed) > 0)

        def test_crypto_verify_hash(self):
            """Test CryptoUtils.verify_hash method"""
            test_string = "Hello, World!"
            hashed = CryptoUtils.hash(test_string)
            self.assertTrue(CryptoUtils.verify_hash(test_string, hashed))
            self.assertFalse(CryptoUtils.verify_hash("Different string", hashed))


class TestEmailUtils(unittest.TestCase):
    """Test email utils module"""

    if EmailUtils:

        def test_email_is_valid(self):
            """Test EmailUtils.is_valid method"""
            # Test valid emails
            self.assertTrue(EmailUtils.is_valid("test@example.com"))
            self.assertTrue(EmailUtils.is_valid("user.name@domain.co.uk"))
            # Test invalid emails
            self.assertFalse(EmailUtils.is_valid("invalid-email"))
            self.assertFalse(EmailUtils.is_valid("test@"))
            self.assertFalse(EmailUtils.is_valid("@example.com"))


class TestFileUtils(unittest.TestCase):
    """Test file utils module"""

    if FileUtils:

        def setUp(self):
            """Set up test fixtures"""
            import tempfile

            self.temp_dir = tempfile.mkdtemp()
            self.test_file = os.path.join(self.temp_dir, "test.txt")
            with open(self.test_file, "w") as f:
                f.write("Test content")

        def tearDown(self):
            """Clean up test fixtures"""
            import shutil

            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

        def test_file_exists(self):
            """Test FileUtils.exists method"""
            self.assertTrue(FileUtils.exists(self.test_file))
            self.assertFalse(FileUtils.exists("non_existent_file_12345.txt"))

        def test_file_read(self):
            """Test FileUtils.read method"""
            content = FileUtils.read(self.test_file)
            self.assertEqual(content, "Test content")

        def test_file_write(self):
            """Test FileUtils.write method"""
            new_content = "New test content"
            FileUtils.write(self.test_file, new_content)
            with open(self.test_file, "r") as f:
                content = f.read()
            self.assertEqual(content, new_content)


class TestHttpUtils(unittest.TestCase):
    """Test http utils module"""

    if HttpUtils:

        @patch("app.utils.http_utils.requests.get")
        def test_http_get(self, mock_get):
            """Test HttpUtils.get method"""
            # Set up mock
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "Test response"
            mock_get.return_value = mock_response

            # Test get method
            response = HttpUtils.get("https://example.com")
            self.assertEqual(response, "Test response")
            mock_get.assert_called_once_with("https://example.com", timeout=10)

        @patch("app.utils.http_utils.requests.post")
        def test_http_post(self, mock_post):
            """Test HttpUtils.post method"""
            # Set up mock
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "Test response"
            mock_post.return_value = mock_response

            # Test post method
            data = {"key": "value"}
            response = HttpUtils.post("https://example.com", data)
            self.assertEqual(response, "Test response")
            mock_post.assert_called_once()


class TestJsonUtils(unittest.TestCase):
    """Test json utils module"""

    if JsonUtils:

        def test_json_dumps(self):
            """Test JsonUtils.dumps method"""
            test_data = {"key": "value", "number": 42}
            json_string = JsonUtils.dumps(test_data)
            self.assertIsInstance(json_string, str)
            # Verify loading gives back original
            loaded_data = json.loads(json_string)
            self.assertEqual(loaded_data, test_data)

        def test_json_loads(self):
            """Test JsonUtils.loads method"""
            test_data = {"key": "value", "number": 42}
            json_string = json.dumps(test_data)
            loaded_data = JsonUtils.loads(json_string)
            self.assertIsInstance(loaded_data, dict)
            self.assertEqual(loaded_data, test_data)


class TestLogger(unittest.TestCase):
    """Test logger module"""

    if Logger:

        def test_logger_get_instance(self):
            """Test Logger.get_instance method"""
            logger = Logger.get_instance()
            self.assertIsInstance(logger, Logger)

        def test_logger_singleton(self):
            """Test Logger singleton pattern"""
            logger1 = Logger.get_instance()
            logger2 = Logger.get_instance()
            self.assertEqual(logger1, logger2)


class TestRandomUtils(unittest.TestCase):
    """Test random utils module"""

    if RandomUtils:

        def test_random_string(self):
            """Test RandomUtils.string method"""
            random_str = RandomUtils.string(10)
            self.assertIsInstance(random_str, str)
            self.assertEqual(len(random_str), 10)

        def test_random_integer(self):
            """Test RandomUtils.integer method"""
            random_int = RandomUtils.integer(1, 10)
            self.assertIsInstance(random_int, int)
            self.assertTrue(1 <= random_int <= 10)


class TestStringUtils(unittest.TestCase):
    """Test string utils module"""

    if StringUtils:

        def test_string_truncate(self):
            """Test StringUtils.truncate method"""
            test_string = "Hello, World!"
            truncated = StringUtils.truncate(test_string, 5)
            self.assertIsInstance(truncated, str)
            self.assertEqual(len(truncated), 5)

        def test_string_capitalize(self):
            """Test StringUtils.capitalize method"""
            test_string = "hello world"
            capitalized = StringUtils.capitalize(test_string)
            self.assertIsInstance(capitalized, str)
            self.assertEqual(capitalized, "Hello world")


class TestTimeUtils(unittest.TestCase):
    """Test time utils module"""

    if TimeUtils:

        def test_time_now(self):
            """Test TimeUtils.now method"""
            now = TimeUtils.now()
            self.assertIsInstance(now, str)
            self.assertTrue(len(now) > 0)

        def test_time_format(self):
            """Test TimeUtils.format method"""
            test_time = time.time()
            formatted = TimeUtils.format(test_time)
            self.assertIsInstance(formatted, str)
            self.assertTrue(len(formatted) > 0)


if __name__ == "__main__":
    unittest.main()
