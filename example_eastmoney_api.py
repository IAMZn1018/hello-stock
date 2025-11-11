"""
东方财富 API 使用示例
"""
from app.utils.eastmoney_api import EastMoneyAPI


def example_get_stock_list():
    """获取股票列表示例"""
    print("=" * 50)
    print("示例 1: 获取股票列表")
    print("=" * 50)
    
    # 创建 API 实例
    api = EastMoneyAPI()
    
    # 获取第 2 页的股票列表，每页 100 条
    result = api.get_stock_list(pn=2, pz=100)
    
    if result:
        print("请求成功！")
        print(f"返回数据: {result}")
    else:
        print("请求失败！")


def example_get_stock_history():
    """获取个股历史股价示例"""
    print("\n" + "=" * 50)
    print("示例 2: 获取个股历史股价")
    print("=" * 50)
    
    # 创建 API 实例
    api = EastMoneyAPI()
    
    # 获取股票代码 300059 最近 30 天的历史数据
    result = api.get_stock_history(secid="0.300059", lmt=30)
    
    if result:
        print("请求成功！")
        print(f"返回数据: {result}")
    else:
        print("请求失败！")


def example_with_custom_cookie():
    """使用自定义 cookie 的示例"""
    print("\n" + "=" * 50)
    print("示例 3: 使用自定义 cookie")
    print("=" * 50)
    
    # 创建 API 实例
    api = EastMoneyAPI()
    
    # 使用自定义 cookie
    my_cookie = "your_cookie_string_here"
    result = api.get_stock_list(pn=1, pz=50, cookie=my_cookie)
    
    if result:
        print("使用自定义 cookie 请求成功！")
    else:
        print("请求失败！")


def example_cookie_management():
    """Cookie 管理示例"""
    print("\n" + "=" * 50)
    print("示例 4: Cookie 管理")
    print("=" * 50)
    
    # 创建 API 实例
    api = EastMoneyAPI()
    
    # 添加 cookie
    api.add_cookie("cookie_1")
    api.add_cookie("cookie_2")
    print(f"当前存储的 cookies: {api.get_all_cookies()}")
    
    # 发起请求（会自动使用存储的 cookie）
    result = api.get_stock_list(pn=1, pz=10)
    
    # 如果请求失败，失效的 cookie 会被自动删除
    print(f"请求后的 cookies: {api.get_all_cookies()}")
    
    # 清空所有 cookies
    # api.clear_cookies()


if __name__ == "__main__":
    # 运行示例
    example_get_stock_list()
    example_get_stock_history()
    example_with_custom_cookie()
    example_cookie_management()

