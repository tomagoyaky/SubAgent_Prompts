import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.llms.basic_provider import BasicProvider

# Try to import all providers
try:
    from app.llms.gpt_provider import GPTProvider
except ImportError:
    GPTProvider = None

try:
    from app.llms.claude_provider import ClaudeProvider
except ImportError:
    ClaudeProvider = None

try:
    from app.llms.ollama_provider import OllamaProvider
except ImportError:
    OllamaProvider = None

try:
    from app.llms.qwen_provider import QwenProvider
except ImportError:
    QwenProvider = None

try:
    from app.llms.doubao_provider import DoubaoProvider
except ImportError:
    DoubaoProvider = None

try:
    from app.llms.deepseek_provider import DeepSeekProvider
except ImportError:
    DeepSeekProvider = None

try:
    from app.llms.glm_provider import GLMProvider
except ImportError:
    GLMProvider = None

try:
    from app.llms.kimi_provider import KimiProvider
except ImportError:
    KimiProvider = None

try:
    from app.llms.minipro_provider import MiniProProvider
except ImportError:
    MiniProProvider = None


class TestBasicProvider(unittest.TestCase):
    """Test basic provider module"""

    def test_basic_provider_initialization(self):
        """Test BasicProvider initialization"""

        # Create a concrete subclass of BasicProvider for testing
        class ConcreteProvider(BasicProvider):
            def _create_llm(self):
                return MagicMock()

            def _generate(self, user_input, system_prompt, **kwargs):
                return "Test response"

            def _stream(self, user_input, system_prompt, **kwargs):
                yield "Test"
                yield " response"

        provider = ConcreteProvider(
            model_name="test-model",
            api_key="test-api-key",
            api_base="https://api.example.com",
            stream_mode=True,
            thinking_mode=True,
            param1="value1",
        )

        self.assertIsInstance(provider, BasicProvider)
        self.assertEqual(provider.model_name, "test-model")
        self.assertEqual(provider.api_key, "test-api-key")
        self.assertEqual(provider.api_base, "https://api.example.com")
        self.assertTrue(provider.stream_mode)
        self.assertTrue(provider.thinking_mode)
        self.assertEqual(provider.kwargs["param1"], "value1")

    def test_basic_provider_chat_generate(self):
        """Test BasicProvider chat method with generate"""

        class ConcreteProvider(BasicProvider):
            def _create_llm(self):
                return MagicMock()

            def _generate(self, user_input, system_prompt, **kwargs):
                return f"Response to: {user_input}"

            def _stream(self, user_input, system_prompt, **kwargs):
                yield "Test"

        provider = ConcreteProvider(
            model_name="test-model", api_key="test-api-key", stream_mode=False
        )

        response = provider.chat("Hello", "You are a helpful assistant")
        self.assertEqual(response, "Response to: Hello")

    def test_basic_provider_chat_stream(self):
        """Test BasicProvider chat method with stream"""

        class ConcreteProvider(BasicProvider):
            def _create_llm(self):
                return MagicMock()

            def _generate(self, user_input, system_prompt, **kwargs):
                return "Test response"

            def _stream(self, user_input, system_prompt, **kwargs):
                yield "Hello"
                yield " world"

        provider = ConcreteProvider(
            model_name="test-model", api_key="test-api-key", stream_mode=True
        )

        response = provider.chat("Hello", "You are a helpful assistant")
        chunks = list(response)
        self.assertEqual(chunks, ["Hello", " world"])

    def test_basic_provider_get_model_info(self):
        """Test BasicProvider get_model_info method"""

        class ConcreteProvider(BasicProvider):
            def _create_llm(self):
                return MagicMock()

            def _generate(self, user_input, system_prompt, **kwargs):
                return "Test response"

            def _stream(self, user_input, system_prompt, **kwargs):
                yield "Test"

        provider = ConcreteProvider(
            model_name="test-model",
            api_key="test-api-key",
            api_base="https://api.example.com",
            stream_mode=True,
            thinking_mode=True,
            param1="value1",
        )

        info = provider.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["api_base"], "https://api.example.com")
        self.assertTrue(info["stream_mode"])
        self.assertTrue(info["thinking_mode"])
        self.assertEqual(info["kwargs"]["param1"], "value1")


# Test individual providers if they are available

if GPTProvider:

    class TestGPTProvider(unittest.TestCase):
        """Test GPT provider module"""

        @patch("app.llms.gpt_provider.ChatOpenAI")
        def test_gpt_provider_initialization(self, mock_chat_openai):
            """Test GPTProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = GPTProvider(
                model_name="gpt-3.5-turbo",
                api_key="test-api-key",
                api_base="https://api.example.com",
            )

            # Check initialization
            self.assertIsInstance(provider, GPTProvider)
            self.assertEqual(provider.model_name, "gpt-3.5-turbo")
            mock_chat_openai.assert_called_once()


if ClaudeProvider:

    class TestClaudeProvider(unittest.TestCase):
        """Test Claude provider module"""

        @patch("app.llms.claude_provider.ChatAnthropic")
        def test_claude_provider_initialization(self, mock_chat_anthropic):
            """Test ClaudeProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_anthropic.return_value = mock_llm

            # Create provider
            provider = ClaudeProvider(
                model_name="claude-3-sonnet-20240229", api_key="test-api-key"
            )

            # Check initialization
            self.assertIsInstance(provider, ClaudeProvider)
            self.assertEqual(provider.model_name, "claude-3-sonnet-20240229")
            mock_chat_anthropic.assert_called_once()


if OllamaProvider:

    class TestOllamaProvider(unittest.TestCase):
        """Test Ollama provider module"""

        @patch("app.llms.ollama_provider.ChatOllama")
        def test_ollama_provider_initialization(self, mock_chat_ollama):
            """Test OllamaProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_ollama.return_value = mock_llm

            # Create provider
            provider = OllamaProvider(
                model_name="llama3",
                api_key="",  # Ollama doesn't require API key
                api_base="http://localhost:11434",
            )

            # Check initialization
            self.assertIsInstance(provider, OllamaProvider)
            self.assertEqual(provider.model_name, "llama3")
            mock_chat_ollama.assert_called_once()


if QwenProvider:

    class TestQwenProvider(unittest.TestCase):
        """Test Qwen provider module"""

        @patch("app.llms.qwen_provider.ChatOpenAI")
        def test_qwen_provider_initialization(self, mock_chat_openai):
            """Test QwenProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = QwenProvider(
                model_name="qwen-turbo",
                api_key="test-api-key",
                api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            # Check initialization
            self.assertIsInstance(provider, QwenProvider)
            self.assertEqual(provider.model_name, "qwen-turbo")
            mock_chat_openai.assert_called_once()


if DoubaoProvider:

    class TestDoubaoProvider(unittest.TestCase):
        """Test Doubao provider module"""

        @patch("app.llms.doubao_provider.ChatOpenAI")
        def test_doubao_provider_initialization(self, mock_chat_openai):
            """Test DoubaoProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = DoubaoProvider(
                model_name="ep-20240528180446-k2456",
                api_key="test-api-key",
                api_base="https://ark.cn-beijing.volces.com/api/v3",
            )

            # Check initialization
            self.assertIsInstance(provider, DoubaoProvider)
            self.assertEqual(provider.model_name, "ep-20240528180446-k2456")
            mock_chat_openai.assert_called_once()


if DeepSeekProvider:

    class TestDeepSeekProvider(unittest.TestCase):
        """Test DeepSeek provider module"""

        @patch("app.llms.deepseek_provider.ChatOpenAI")
        def test_deepseek_provider_initialization(self, mock_chat_openai):
            """Test DeepSeekProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = DeepSeekProvider(
                model_name="deepseek-chat",
                api_key="test-api-key",
                api_base="https://api.deepseek.com/v1",
            )

            # Check initialization
            self.assertIsInstance(provider, DeepSeekProvider)
            self.assertEqual(provider.model_name, "deepseek-chat")
            mock_chat_openai.assert_called_once()


if GLMProvider:

    class TestGLMProvider(unittest.TestCase):
        """Test GLM provider module"""

        @patch("app.llms.glm_provider.ChatOpenAI")
        def test_glm_provider_initialization(self, mock_chat_openai):
            """Test GLMProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = GLMProvider(
                model_name="glm-4",
                api_key="test-api-key",
                api_base="https://open.bigmodel.cn/api/mcp",
            )

            # Check initialization
            self.assertIsInstance(provider, GLMProvider)
            self.assertEqual(provider.model_name, "glm-4")
            mock_chat_openai.assert_called_once()


if KimiProvider:

    class TestKimiProvider(unittest.TestCase):
        """Test Kimi provider module"""

        @patch("app.llms.kimi_provider.ChatOpenAI")
        def test_kimi_provider_initialization(self, mock_chat_openai):
            """Test KimiProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = KimiProvider(
                model_name="kimi-k2",
                api_key="test-api-key",
                api_base="https://api.moonshot.cn/v1",
            )

            # Check initialization
            self.assertIsInstance(provider, KimiProvider)
            self.assertEqual(provider.model_name, "kimi-k2")
            mock_chat_openai.assert_called_once()


if MiniProProvider:

    class TestMiniProProvider(unittest.TestCase):
        """Test MiniPro provider module"""

        @patch("app.llms.minipro_provider.ChatOpenAI")
        def test_minipro_provider_initialization(self, mock_chat_openai):
            """Test MiniProProvider initialization"""
            # Set up mock
            mock_llm = MagicMock()
            mock_chat_openai.return_value = mock_llm

            # Create provider
            provider = MiniProProvider(
                model_name="minipro",
                api_key="test-api-key",
                api_base="https://api.minipro.ai/v1",
            )

            # Check initialization
            self.assertIsInstance(provider, MiniProProvider)
            self.assertEqual(provider.model_name, "minipro")
            mock_chat_openai.assert_called_once()


if __name__ == "__main__":
    unittest.main()
