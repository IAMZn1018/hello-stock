"""
东方财富 API 封装
提供股票列表和历史股价查询功能
"""
import requests
from typing import Optional, Dict, Any
from .cookie_manager import CookieManager


class EastMoneyAPI:
    """东方财富 API 封装类"""
    
    # 默认请求头
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
    }
    
    # API 端点
    STOCK_LIST_URL = 'http://push2.eastmoney.com/api/qt/clist/get'
    STOCK_KLINE_URL = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
    
    def __init__(self, cookie_file: str = "eastmoney_cookies.json"):
        """
        初始化东方财富 API
        
        Args:
            cookie_file: cookie 存储文件路径
        """
        self.cookie_manager = CookieManager(cookie_file)
    
    def _make_request(self, url: str, params: Dict[str, Any], custom_cookie: Optional[str] = None) -> Optional[Dict]:
        """
        发起请求的通用方法
        
        Args:
            url: 请求 URL
            params: 请求参数
            custom_cookie: 自定义 cookie，如果不提供则从 cookie 管理器获取
        
        Returns:
            响应的 JSON 数据，如果请求失败返回 None
        """
        # 准备 headers
        headers = self.DEFAULT_HEADERS.copy()
        
        # 获取 cookie
        cookie = custom_cookie if custom_cookie else self.cookie_manager.get_cookie()
        if cookie:
            headers['Cookie'] = cookie
        
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as e:
            # 如果请求失败且使用了 cookie，则删除该 cookie
            if cookie and not custom_cookie:
                self.cookie_manager.remove_cookie(cookie)
            print(f"请求失败: {e}")
            return None
    
    def get_stock_list(self, 
                       pn: int = 1, 
                       pz: int = 100,
                       po: int = 1,
                       np: int = 1,
                       cookie: Optional[str] = None) -> Optional[Dict]:
        """
        获取股票列表
        
        Args:
            pn: 页码 (page num)，默认为 1
            pz: 每页数量 (page size)，默认为 100
            po: 排序方式，0：升序 1：降序，默认为 1
            np: 序号显示，0带序号 1不带序号 2全部带序号 3全部不带序号，默认为 1
            cookie: 自定义 cookie，可选
        
        Returns:
            股票列表数据的 JSON 响应，失败返回 None
            
        Example:
            >>> api = EastMoneyAPI()
            >>> result = api.get_stock_list(pn=2, pz=100)
            >>> if result:
            >>>     print(result)
        """
        params = {
            'pn': pn,
            'pz': pz,
            'po': po,
            'np': np,
            'fltt': 2,
            'invt': 2,
            'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
            'fields': 'f12,f13,f14,f3,f4,f5,f6,f7,f8,f15,f16,f17,f18'
        }
        
        return self._make_request(self.STOCK_LIST_URL, params, cookie)
    
    def get_stock_history(self,
                         secid: str,
                         lmt: int = 210,
                         klt: str = '101',
                         fqt: int = 1,
                         cookie: Optional[str] = None) -> Optional[Dict]:
        """
        获取个股历史股价
        
        Args:
            secid: 市场代码.股票代码，例如: "0.300059"
            lmt: 限制返回的数据条数，从现在往前 lmt 天，默认为 210
            klt: K线类型，101表示日K线，默认为 '101'
            fqt: 复权类型，0不复权 1前复权 2后复权，默认为 1
            cookie: 自定义 cookie，可选
        
        Returns:
            历史股价数据的 JSON 响应，失败返回 None
            
        Example:
            >>> api = EastMoneyAPI()
            >>> result = api.get_stock_history(secid="0.300059", lmt=30)
            >>> if result:
            >>>     print(result)
        """
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': klt,
            'fqt': fqt,
            'secid': secid,
            'lmt': lmt,
            'end': '20500000'
        }
        
        return self._make_request(self.STOCK_KLINE_URL, params, cookie)
    
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

