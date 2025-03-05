import os
import unittest
from unittest.mock import patch, MagicMock
from installer import install_tool, remove_tool

class TestInstaller(unittest.TestCase):

    @patch('installer.download_file')
    @patch('installer.extract_tarball')
    @patch('installer.system_info', return_value=('Linux', 'x86_64'))
    @patch('os.makedirs')
    @patch('os.remove')
    @patch('os.rename')
    @patch('os.path.exists', return_value=True)
    def test_install_tool(self, mock_exists, mock_rename, mock_remove, mock_makedirs, mock_system_info, mock_extract_tarball, mock_download_file):
        tool = 'obsidian'
        version = 'v1.0.0'
        home_dir = os.getenv("HOME")
        extraction_dir = os.path.join(home_dir, ".ember", tool)
        original_exec = os.path.join(extraction_dir, f"{tool}-linux-x86_64")
        new_exec = os.path.join(extraction_dir, f"{tool}-linux-x86_64-{version}")

        install_tool(tool, version)

        mock_download_file.assert_called_once_with(f"https://github.com/obsidian-language/{tool}/releases/download/{version}/{tool}-Linux-x86_64.tar.gz", f"{tool}.tar.gz")
        mock_extract_tarball.assert_called_once_with(f"{tool}.tar.gz", extraction_dir)
        mock_remove.assert_called_once_with(f"{tool}.tar.gz")
        mock_rename.assert_called_once_with(original_exec, new_exec)

    @patch('installer.system_info', return_value=('Linux', 'x86_64'))
    @patch('os.remove')
    @patch('os.path.exists', return_value=True)
    def test_remove_tool(self, mock_exists, mock_remove, mock_system_info):
        tool = 'obsidian'
        version = 'v1.0.0'
        home_dir = os.getenv("HOME")
        tool_exec = os.path.join(home_dir, ".ember", tool, f"{tool}-linux-x86_64-{version}")

        remove_tool(tool, version)

        mock_remove.assert_called_once_with(tool_exec)

if __name__ == '__main__':
    unittest.main()