"""
HFPics
======

一个用于从Hugging Face数据集下载图片的Python包。

基本用法:
    >>> from hfpics import HfPics
    >>> hf = HfPics()
    >>> image_path = hf.pic(11112)
"""

from .core import HfPics

__version__ = "0.1.0" 