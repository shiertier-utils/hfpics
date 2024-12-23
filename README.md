# HFPics

一个简单的Python包，用于从Hugging Face数据集下载图片。

## 安装

```bash
pip install hfpics
```

## 使用方法

```python
from hfpics import HfPics

# 使用默认配置
hf = HfPics()

# 或使用自定义配置
hf = HfPics(
    repo="picollect/a_1024",  # 自定义数据集仓库
    cache_dir="/custom/path"   # 自定义缓存目录
)

# 下载图片并获取路径
image_path = hf.pic(11112)
print(f"图片保存在: {image_path}")

# 直接获取图片内容
image_content = hf.pic(11112, return_type="content")
```

## 功能特点

- 支持从Hugging Face数据集下载图片
- 自动缓存已下载的图片
- 支持返回图片路径或二进制内容
- 支持.jpg和.webp格式
- 支持自定义缓存目录

## API文档

### HfPics类

```python
HfPics(repo: str = "picollect/a_1024", cache_dir: str = "~/.cache/hf_pics")
```

参数:
- `repo`: Hugging Face数据集仓库名称，默认"picollect/a_1024"，为a站数据集
- `cache_dir`: 缓存目录路径，默认"~/.cache/hf_pics"

### pic方法

```python
pic(id: int, return_type: Literal["path", "content"] = "path") -> Union[str, bytes, None]
```

参数:
- `id`: 图片ID（整数）
- `return_type`: 返回类型
  - "path": 返回图片文件路径（默认）
  - "content": 返回图片二进制内容

返回值:
- 当 return_type="path" 时返回字符串路径
- 当 return_type="content" 时返回字节内容
- 如果图片不存在返回 None

## 异常处理

```python
try:
    image = hf.pic(11112)
except ValueError as e:
    print(f"参数错误: {e}")
except Exception as e:
    print(f"下载失败: {e}")
```

## 许可证

MIT License