import pytest
from downloader import download_file

def test_download_file(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.iter_content = lambda chunk_size: [b'Test data']

    download_file('http://example.com/testfile', 'testfile')

    with open('testfile', 'rb') as f:
        data = f.read()
        assert data == b'Test data'
