import pytest
import os
from pathlib import Path
from hfpics import HfPics
from hfpics.core import get_key_str, fetch_json, find_target_file

def test_hfpics_init():
    hf = HfPics()
    assert hf.repo == "picollect/a_1024"
    assert hf.base_url == "https://huggingface.co/datasets/picollect/a_1024/resolve/main"
    assert os.path.exists(os.path.expanduser("~/.cache/hf_pics"))

def test_custom_init():
    custom_cache = "/tmp/test_hfpics"
    hf = HfPics(repo="custom/repo", cache_dir=custom_cache)
    assert hf.repo == "custom/repo"
    assert hf.cache_dir == custom_cache
    assert os.path.exists(custom_cache)
    
def test_invalid_return_type():
    hf = HfPics()
    with pytest.raises(ValueError, match="return_type 必须为 'path' 或 'content'"):
        hf.pic(11112, return_type="invalid")

def test_get_key_str():
    assert get_key_str(11112) == "0001"
    assert get_key_str(20000) == "0002"
    assert get_key_str(123456) == "0012"
    assert get_key_str(0) == "0000"

def test_find_target_file():
    files = {
        "11112.jpg": {"offset": 0, "size": 100},
        "11113.webp": {"offset": 100, "size": 200},
        "other.txt": {"offset": 300, "size": 50}
    }
    
    result = find_target_file(files, "11112")
    assert result == ("11112.jpg", {"offset": 0, "size": 100})
    
    result = find_target_file(files, "11113")
    assert result == ("11113.webp", {"offset": 100, "size": 200})
    
    result = find_target_file(files, "99999")
    assert result is None

@pytest.fixture
def mock_requests(monkeypatch):
    class MockResponse:
        def __init__(self, content=b"test", status_code=200):
            self.content = content
            self.status_code = status_code
            
        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("HTTP Error")
                
        def json(self):
            return {"files": {"11112.jpg": {"offset": 0, "size": 100}}}
            
    def mock_get(*args, **kwargs):
        return MockResponse()
        
    monkeypatch.setattr("requests.get", mock_get)
    return mock_get

def test_fetch_json(mock_requests):
    result = fetch_json("http://test.com")
    assert isinstance(result, dict)
    assert "files" in result

def test_cache_path():
    hf = HfPics(cache_dir="/tmp/test_hfpics")
    path = hf.get_cache_path(11112)
    assert isinstance(path, Path)
    assert str(path) == "/tmp/test_hfpics/11112"

@pytest.mark.integration
def test_real_download():
    """实际下载测试，默认跳过"""
    pytest.skip("跳过实际下载测试")
    hf = HfPics()
    result = hf.pic(11112)
    assert result is not None
    assert os.path.exists(result)