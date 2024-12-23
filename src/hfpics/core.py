"""
HFPics - 一个用于从Hugging Face数据集下载图片的Python包
"""

import os
import requests
import json
from pathlib import Path
from typing import Union, Tuple, Literal

def get_key_str(id: int) -> str:
    key_num = id // 10000
    return str(key_num).zfill(4)

def fetch_json(url: str) -> dict:
    """
    从URL获取JSON数据
    
    Args:
        url: JSON数据的URL
        
    Returns:
        解析后的JSON数据
        
    Raises:
        Exception: 当请求失败或JSON解析失败时
    """
    try:
        response = requests.get(url, timeout=10)  # 添加超时
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("请求超时")
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("JSON解析失败")
    except Exception as e:
        raise Exception(f"获取JSON数据失败: {str(e)}")

def find_target_file(files: dict, target_id: str) -> tuple:
    for filename, file_info in files.items():
        if filename.startswith(target_id) and (filename.endswith('.jpg') or filename.endswith('.webp')):
            return filename, file_info
    return None

def download_file_range(url: str, offset: int, size: int) -> bytes:
    """
    下载文件的指定字节范围
    
    Args:
        url: 文件URL
        offset: 起始字节位置
        size: 要下载的字节数
        
    Returns:
        下载的字节内容
        
    Raises:
        Exception: 当下载失败时
    """
    headers = {'Range': f'bytes={offset}-{offset+size-1}'}
    try:
        response = requests.get(url, headers=headers, timeout=30)  # 增加下载超时时间
        response.raise_for_status()
        return response.content
    except requests.exceptions.Timeout:
        raise Exception("下载超时")
    except requests.exceptions.RequestException as e:
        raise Exception(f"下载失败: {str(e)}")
    except Exception as e:
        raise Exception(f"未知错误: {str(e)}")

class HfPics:
    """
    用于从Hugging Face数据集下载和缓存图片的类
    
    Args:
        repo (str): Hugging Face数据集仓库名称
        cache_dir (str): 图片缓存目录路径
    """
    
    def __init__(self, repo="picollect/a_1024", cache_dir="~/.cache/hf_pics"):
        self.repo = repo
        self.base_url = f"https://huggingface.co/datasets/{repo}/resolve/main"
        self.cache_dir = os.path.expanduser(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_path(self, id: int) -> Path:
        return Path(self.cache_dir) / str(id)
    
    def pic(self, id: int, return_type: Literal["path", "content"] = "path") -> Union[str, bytes, None]:
        """
        下载并获取指定ID的图片
        
        Args:
            id (int): 图片ID
            return_type (Literal["path", "content"]): 返回类型，"path"返回文件路径，"content"返回二进制内容
            
        Returns:
            Union[str, bytes, None]: 根据return_type返回文件路径或二进制内容，如果图片不存在则返回None
            
        Raises:
            ValueError: 当return_type不是"path"或"content"时
        """
        if return_type not in ["path", "content"]:
            raise ValueError("return_type 必须为 'path' 或 'content'")
            
        cache_path = self.get_cache_path(id)
        if cache_path.exists():
            if return_type == "path":
                return str(cache_path)
            else:  # content
                with open(cache_path, 'rb') as f:
                    return f.read()
        
        key_str = get_key_str(id)
        index_url = f"{self.base_url}/index/{key_str}.json"
        index_data = fetch_json(index_url)
        
        target_file = find_target_file(index_data.get("files", {}), str(id))
        if not target_file:
            print(f"ID {id} 无对应的图片")
            return None
            
        filename, file_info = target_file
        
        tar_url = f"{self.base_url}/images/{key_str}.tar"
        content = download_file_range(tar_url, file_info['offset'], file_info['size'])
        
        extension = '.webp' if filename.endswith('.webp') else '.jpg'
        cache_path = cache_path.with_suffix(extension)
        
        with open(cache_path, 'wb') as f:
            f.write(content)
        
        return str(cache_path) if return_type == "path" else content

# hf = HfPics()  # 使用默认缓存目录
# 或
# hf = HfPics(repo="picollect/a_1024", cache_dir="/root")  # 使用自定义缓存目录
# image_path = hf.pic(11112)
# print(f"图片保存在: {image_path}")