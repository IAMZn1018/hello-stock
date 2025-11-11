"""
Cookie 管理器
用于管理和持久化 cookie
"""
import json
import os
from typing import Optional, List
from pathlib import Path


class CookieManager:
    """Cookie 管理器，负责 cookie 的存储、读取和删除"""
    
    def __init__(self, cookie_file: str = "cookies.json"):
        """
        初始化 Cookie 管理器
        
        Args:
            cookie_file: cookie 存储文件路径
        """
        self.cookie_file = Path(cookie_file)
        self._ensure_cookie_file()
    
    def _ensure_cookie_file(self):
        """确保 cookie 文件存在"""
        if not self.cookie_file.exists():
            self.cookie_file.write_text(json.dumps([]))
    
    def get_cookie(self) -> Optional[str]:
        """
        获取一个可用的 cookie
        
        Returns:
            cookie 字符串，如果没有可用的 cookie 则返回 None
        """
        cookies = self._load_cookies()
        if cookies:
            return cookies[0]
        return None
    
    def add_cookie(self, cookie: str):
        """
        添加一个新的 cookie
        
        Args:
            cookie: cookie 字符串
        """
        if not cookie:
            return
        
        cookies = self._load_cookies()
        if cookie not in cookies:
            cookies.append(cookie)
            self._save_cookies(cookies)
    
    def remove_cookie(self, cookie: str):
        """
        删除一个失效的 cookie
        
        Args:
            cookie: 要删除的 cookie 字符串
        """
        cookies = self._load_cookies()
        if cookie in cookies:
            cookies.remove(cookie)
            self._save_cookies(cookies)
    
    def _load_cookies(self) -> List[str]:
        """
        从文件加载所有 cookies
        
        Returns:
            cookie 列表
        """
        try:
            content = self.cookie_file.read_text()
            return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_cookies(self, cookies: List[str]):
        """
        保存 cookies 到文件
        
        Args:
            cookies: cookie 列表
        """
        self.cookie_file.write_text(json.dumps(cookies, indent=2))
    
    def get_all_cookies(self) -> List[str]:
        """
        获取所有存储的 cookies
        
        Returns:
            cookie 列表
        """
        return self._load_cookies()
    
    def clear_all_cookies(self):
        """清空所有 cookies"""
        self._save_cookies([])

