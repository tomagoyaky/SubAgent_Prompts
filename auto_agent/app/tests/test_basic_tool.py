import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import the actual functions instead of the decorated tools
from app.agents.tools.basic_tool import BasicTool
from app.agents.tools.basic_tool import delete_directory as _delete_directory
from app.agents.tools.basic_tool import delete_file as _delete_file
from app.agents.tools.basic_tool import edit_file as _edit_file
from app.agents.tools.basic_tool import edit_file_line as _edit_file_line
from app.agents.tools.basic_tool import execute_command as _execute_command
from app.agents.tools.basic_tool import execute_python as _execute_python
from app.agents.tools.basic_tool import get_all_tools
from app.agents.tools.basic_tool import list_files as _list_files
from app.agents.tools.basic_tool import read_file as _read_file
from app.agents.tools.basic_tool import web_search as _web_search
from app.agents.tools.basic_tool import write_file as _write_file


class TestBasicTool(unittest.TestCase):
    """Test basic tool module"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for file operations
        self.temp_dir = tempfile.mkdtemp()

        # Create a test file
        self.test_file = os.path.join(self.temp_dir, "test.txt")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Line 1\nLine 2\nLine 3\n")

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary directory
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_basic_tool_initialization(self):
        """Test BasicTool initialization"""

        # Create a concrete subclass of BasicTool
        class ConcreteTool(BasicTool):
            def run(self, *args, **kwargs):
                return {"result": "test"}

        tool = ConcreteTool("Test Tool", "A test tool", param1="value1")
        self.assertIsInstance(tool, BasicTool)
        self.assertEqual(tool.name, "Test Tool")
        self.assertEqual(tool.description, "A test tool")

    def test_basic_tool_get_info(self):
        """Test BasicTool get_info method"""

        class ConcreteTool(BasicTool):
            def run(self, *args, **kwargs):
                return {"result": "test"}

        tool = ConcreteTool("Test Tool", "A test tool", param1="value1")
        info = tool.get_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info["name"], "Test Tool")
        self.assertEqual(info["description"], "A test tool")
        self.assertEqual(info["param1"], "value1")

    def test_basic_tool_validate_input(self):
        """Test BasicTool validate_input method"""

        class ConcreteTool(BasicTool):
            def run(self, *args, **kwargs):
                return {"result": "test"}

        tool = ConcreteTool("Test Tool", "A test tool")
        self.assertTrue(tool.validate_input())
        self.assertTrue(tool.validate_input("test", key="value"))

    def test_list_files(self):
        """Test list_files tool"""
        import asyncio

        result = asyncio.run(_list_files(self.temp_dir))
        self.assertIn("test.txt", result)
        self.assertIn(os.path.basename(self.temp_dir), result)

    def test_list_files_error(self):
        """Test list_files tool with error"""
        import asyncio

        result = asyncio.run(_list_files("non_existent_directory_12345"))
        self.assertIn("Error listing files", result)

    def test_read_file(self):
        """Test read_file tool"""
        import asyncio

        result = asyncio.run(_read_file(self.test_file))
        self.assertEqual(result, "Line 1\nLine 2\nLine 3\n")

    def test_read_file_error(self):
        """Test read_file tool with error"""
        import asyncio

        result = asyncio.run(_read_file("non_existent_file_12345.txt"))
        self.assertIn("Error reading file", result)

    def test_write_file(self):
        """Test write_file tool"""
        import asyncio

        new_file = os.path.join(self.temp_dir, "new_file.txt")
        result = asyncio.run(_write_file(new_file, "Hello, World!"))
        self.assertIn("Successfully wrote to", result)

        # Verify file content
        with open(new_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")

    def test_write_file_overwrite(self):
        """Test write_file tool with overwrite"""
        import asyncio

        result = asyncio.run(
            _write_file(self.test_file, "Overwritten content", overwrite=True)
        )
        self.assertIn("Successfully wrote to", result)

        # Verify file content
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Overwritten content")

    def test_write_file_no_overwrite(self):
        """Test write_file tool without overwrite"""
        import asyncio

        result = asyncio.run(_write_file(self.test_file, "New content"))
        self.assertIn("already exists", result)

    def test_edit_file(self):
        """Test edit_file tool"""
        import asyncio

        result = asyncio.run(_edit_file(self.test_file, "Line 2", "Modified Line 2"))
        self.assertIn("Successfully edited", result)

        # Verify file content
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Modified Line 2", content)

    def test_edit_file_line(self):
        """Test edit_file_line tool"""
        import asyncio

        result = asyncio.run(_edit_file_line(self.test_file, 2, "Modified Line 2"))
        self.assertIn("Successfully edited line 2", result)

        # Verify file content
        with open(self.test_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(lines[1], "Modified Line 2\n")

    def test_edit_file_line_out_of_range(self):
        """Test edit_file_line tool with line out of range"""
        import asyncio

        result = asyncio.run(_edit_file_line(self.test_file, 10, "New Line"))
        self.assertIn("Line number 10 is out of range", result)

    @patch("app.agents.tools.basic_tool.requests.get")
    def test_web_search(self, mock_get):
        """Test web_search tool"""
        import asyncio

        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Abstract": "Test abstract",
            "RelatedTopics": [{"Text": "Topic 1"}, {"Text": "Topic 2"}],
        }
        mock_get.return_value = mock_response

        result = asyncio.run(_web_search("test query"))
        self.assertIn("Test abstract", result)
        self.assertIn("Topic 1", result)
        self.assertIn("Topic 2", result)

    @patch("app.agents.tools.basic_tool.requests.get")
    def test_web_search_no_results(self, mock_get):
        """Test web_search tool with no results"""
        import asyncio

        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = asyncio.run(_web_search("test query"))
        self.assertIn("No results found", result)

    @patch("app.agents.tools.basic_tool.subprocess.run")
    def test_execute_command(self, mock_run):
        """Test execute_command tool"""
        import asyncio

        # Set up mock response
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Command output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = asyncio.run(_execute_command("echo 'test'"))
        self.assertIn("Exit code: 0", result)
        self.assertIn("Command output", result)

    @patch("app.agents.tools.basic_tool.subprocess.run")
    def test_execute_python(self, mock_run):
        """Test execute_python tool"""
        import asyncio

        # Set up mock response
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Python output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = asyncio.run(_execute_python("print('test')"))
        self.assertIn("Exit code: 0", result)
        self.assertIn("Python output", result)

    def test_delete_file(self):
        """Test delete_file tool"""
        import asyncio

        # Create a temporary file to delete
        file_to_delete = os.path.join(self.temp_dir, "delete_me.txt")
        with open(file_to_delete, "w") as f:
            f.write("Delete me")

        result = asyncio.run(_delete_file(file_to_delete))
        self.assertIn("Successfully deleted", result)
        self.assertFalse(os.path.exists(file_to_delete))

    def test_delete_file_not_exists(self):
        """Test delete_file tool with non-existent file"""
        import asyncio

        result = asyncio.run(_delete_file("non_existent_file_12345.txt"))
        self.assertIn("File non_existent_file_12345.txt does not exist", result)

    def test_delete_directory(self):
        """Test delete_directory tool"""
        import asyncio

        # Create a temporary directory to delete
        dir_to_delete = os.path.join(self.temp_dir, "delete_me_dir")
        os.makedirs(dir_to_delete)

        # Create a file in the directory
        with open(os.path.join(dir_to_delete, "test.txt"), "w") as f:
            f.write("Test")

        result = asyncio.run(_delete_directory(dir_to_delete))
        self.assertIn("Successfully deleted directory", result)
        self.assertFalse(os.path.exists(dir_to_delete))

    def test_delete_directory_not_exists(self):
        """Test delete_directory tool with non-existent directory"""
        import asyncio

        result = asyncio.run(_delete_directory("non_existent_dir_12345"))
        self.assertIn("Directory non_existent_dir_12345 does not exist", result)

    def test_get_all_tools(self):
        """Test get_all_tools function"""
        tools = get_all_tools()
        self.assertIsInstance(tools, list)
        self.assertEqual(len(tools), 10)  # Should have 10 tools
        # Check that all expected tools are present
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "list_files",
            "read_file",
            "write_file",
            "edit_file",
            "edit_file_line",
            "web_search",
            "execute_command",
            "execute_python",
            "delete_file",
            "delete_directory",
        ]
        for expected_tool in expected_tools:
            self.assertIn(expected_tool, tool_names)


if __name__ == "__main__":
    unittest.main()
