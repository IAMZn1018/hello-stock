"""
同花顺涨停雷达爬虫
爬取涨停雷达页面并提取相关信息
"""
import requests
from lxml import etree
from typing import List, Dict, Optional
from .cookie_manager import CookieManager


class THSCrawler:
    """同花顺涨停雷达爬虫类"""
    
    # 涨停雷达页面 URL
    LIMIT_UP_RADAR_URL = 'https://yuanchuang.10jqka.com.cn/mrnxgg_list/'
    
    # 默认请求头
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, cookie_file: str = "ths_cookies.json"):
        """
        初始化同花顺爬虫
        
        Args:
            cookie_file: cookie 存储文件路径
        """
        self.cookie_manager = CookieManager(cookie_file)
    
    def _make_request(self, url: str, custom_cookie: Optional[str] = None) -> Optional[str]:
        """
        发起 HTTP 请求
        
        Args:
            url: 请求 URL
            custom_cookie: 自定义 cookie，如果不提供则从 cookie 管理器获取
        
        Returns:
            页面 HTML 内容，如果请求失败返回 None
        """
        # 准备 headers
        headers = self.DEFAULT_HEADERS.copy()
        
        # 获取 cookie
        cookie = custom_cookie if custom_cookie else self.cookie_manager.get_cookie()
        if cookie:
            headers['Cookie'] = cookie
        
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            resp.encoding = 'utf-8'  # 设置编码
            return resp.text
        except requests.RequestException as e:
            # 如果请求失败且使用了 cookie，则删除该 cookie
            if cookie and not custom_cookie:
                self.cookie_manager.remove_cookie(cookie)
            print(f"请求失败: {e}")
            return None
    
    def get_limit_up_news(self, cookie: Optional[str] = None) -> List[Dict[str, str]]:
        """
        获取涨停雷达新闻列表
        
        Args:
            cookie: 自定义 cookie，可选
        
        Returns:
            新闻列表，每个元素包含 time（时间）、title（标题）、data_seq（数据序号）、url（链接）
            
        Example:
            >>> crawler = THSCrawler()
            >>> news_list = crawler.get_limit_up_news()
            >>> for news in news_list:
            >>>     print(f"{news['time']} - {news['title']}")
        """
        # 请求页面
        html_content = self._make_request(self.LIMIT_UP_RADAR_URL, cookie)
        if not html_content:
            return []
        
        # 解析 HTML
        try:
            html = etree.HTML(html_content)
            return self._parse_news_list(html)
        except Exception as e:
            print(f"HTML 解析失败: {e}")
            return []
    
    def _parse_news_list(self, html: etree._Element) -> List[Dict[str, str]]:
        """
        解析新闻列表
        
        Args:
            html: lxml 解析后的 HTML 元素
        
        Returns:
            新闻列表
        """
        news_list = []
        
        # XPath 提取所有新闻条目
        news_items = html.xpath('//div[@class="list-con"]//ul/li')
        
        for item in news_items:
            try:
                # 提取时间 - 在 span.arc-title 下的 span 标签中
                time_elements = item.xpath('.//span[@class="arc-title"]/span/text()')
                time = time_elements[0].strip() if time_elements else ""
                
                # 提取标题和 data-seq - 在 span.arc-title 下的 a 标签中
                title_links = item.xpath('.//span[@class="arc-title"]/a[@class="news-link"]')
                if not title_links:
                    continue
                
                title_link = title_links[0]
                title = title_link.get('title', '').strip()
                data_seq = title_link.get('data-seq', '').strip()
                url = title_link.get('href', '').strip()
                
                # 如果关键字段都存在，则添加到列表
                if time and title and data_seq:
                    news_list.append({
                        'time': time,
                        'title': title,
                        'data_seq': data_seq,
                        'url': url
                    })
            except Exception as e:
                print(f"解析单个新闻条目失败: {e}")
                continue
        
        return news_list
    
    def get_limit_up_news_with_content(self, cookie: Optional[str] = None) -> List[Dict[str, str]]:
        """
        获取涨停雷达新闻列表（包含内容摘要）
        
        Args:
            cookie: 自定义 cookie，可选
        
        Returns:
            新闻列表，每个元素包含 time、title、data_seq、url、content（内容摘要）
        """
        # 请求页面
        html_content = self._make_request(self.LIMIT_UP_RADAR_URL, cookie)
        if not html_content:
            return []
        
        # 解析 HTML
        try:
            html = etree.HTML(html_content)
            return self._parse_news_list_with_content(html)
        except Exception as e:
            print(f"HTML 解析失败: {e}")
            return []
    
    def _parse_news_list_with_content(self, html: etree._Element) -> List[Dict[str, str]]:
        """
        解析新闻列表（包含内容摘要）
        
        Args:
            html: lxml 解析后的 HTML 元素
        
        Returns:
            新闻列表
        """
        news_list = []
        
        # XPath 提取所有新闻条目
        news_items = html.xpath('//div[@class="list-con"]//ul/li')
        
        for item in news_items:
            try:
                # 提取时间
                time_elements = item.xpath('.//span[@class="arc-title"]/span/text()')
                time = time_elements[0].strip() if time_elements else ""
                
                # 提取标题和 data-seq
                title_links = item.xpath('.//span[@class="arc-title"]/a[@class="news-link"]')
                if not title_links:
                    continue
                
                title_link = title_links[0]
                title = title_link.get('title', '').strip()
                data_seq = title_link.get('data-seq', '').strip()
                url = title_link.get('href', '').strip()
                
                # 提取内容摘要
                content_elements = item.xpath('.//a[@class="arc-cont news-link"]/text()')
                content = content_elements[0].strip() if content_elements else ""
                
                # 如果关键字段都存在，则添加到列表
                if time and title and data_seq:
                    news_list.append({
                        'time': time,
                        'title': title,
                        'data_seq': data_seq,
                        'url': url,
                        'content': content
                    })
            except Exception as e:
                print(f"解析单个新闻条目失败: {e}")
                continue
        
        return news_list
    
    def add_cookie(self, cookie: str):
        """
        添加一个新的 cookie
        
        Args:
            cookie: cookie 字符串
        """
        self.cookie_manager.add_cookie(cookie)
    
    def get_all_cookies(self):
        """
        获取所有存储的 cookies
        
        Returns:
            cookie 列表
        """
        return self.cookie_manager.get_all_cookies()
    
    def clear_cookies(self):
        """清空所有 cookies"""
        self.cookie_manager.clear_all_cookies()

