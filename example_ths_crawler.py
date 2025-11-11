"""
同花顺涨停雷达爬虫使用示例
"""
from app.utils.ths_crawler import THSCrawler


def example_get_limit_up_news():
    """获取涨停雷达新闻（基本信息）"""
    print("=" * 80)
    print("示例 1: 获取涨停雷达新闻（时间、标题、data-seq）")
    print("=" * 80)
    
    # 创建爬虫实例
    crawler = THSCrawler()
    
    # 获取新闻列表
    news_list = crawler.get_limit_up_news()
    
    if news_list:
        print(f"\n成功获取 {len(news_list)} 条新闻：\n")
        for i, news in enumerate(news_list, 1):
            print(f"{i}. [{news['time']}] {news['title']}")
            print(f"   data-seq: {news['data_seq']}")
            print(f"   链接: {news['url']}")
            print()
    else:
        print("获取失败或没有新闻数据")


def example_get_limit_up_news_with_content():
    """获取涨停雷达新闻（包含内容摘要）"""
    print("\n" + "=" * 80)
    print("示例 2: 获取涨停雷达新闻（包含内容摘要）")
    print("=" * 80)
    
    # 创建爬虫实例
    crawler = THSCrawler()
    
    # 获取新闻列表（包含内容）
    news_list = crawler.get_limit_up_news_with_content()
    
    if news_list:
        print(f"\n成功获取 {len(news_list)} 条新闻：\n")
        # 只显示前 3 条作为示例
        for i, news in enumerate(news_list[:3], 1):
            print(f"{i}. [{news['time']}] {news['title']}")
            print(f"   data-seq: {news['data_seq']}")
            print(f"   内容摘要: {news['content'][:80]}...")
            print(f"   链接: {news['url']}")
            print()
    else:
        print("获取失败或没有新闻数据")


def example_with_cookie():
    """使用自定义 cookie 的示例"""
    print("\n" + "=" * 80)
    print("示例 3: 使用自定义 cookie")
    print("=" * 80)
    
    # 创建爬虫实例
    crawler = THSCrawler()
    
    # 添加 cookie（如果有的话）
    # crawler.add_cookie("your_cookie_string_here")
    
    # 或者直接在请求时传入 cookie
    # news_list = crawler.get_limit_up_news(cookie="your_cookie_string_here")
    
    # 查看当前存储的 cookies
    print(f"当前存储的 cookies: {crawler.get_all_cookies()}")
    
    # 普通请求
    news_list = crawler.get_limit_up_news()
    print(f"获取到 {len(news_list)} 条新闻")


def example_export_to_dict():
    """导出数据为字典格式"""
    print("\n" + "=" * 80)
    print("示例 4: 导出为结构化数据")
    print("=" * 80)
    
    # 创建爬虫实例
    crawler = THSCrawler()
    
    # 获取新闻列表
    news_list = crawler.get_limit_up_news_with_content()
    
    if news_list:
        # 按 data-seq 建立索引
        news_dict = {news['data_seq']: news for news in news_list}
        
        print(f"共 {len(news_dict)} 条新闻")
        print(f"data-seq 范围: {min(news_dict.keys())} - {max(news_dict.keys())}")
        
        # 示例：查找特定 data-seq 的新闻
        sample_seq = list(news_dict.keys())[0] if news_dict else None
        if sample_seq:
            print(f"\n示例数据（data-seq: {sample_seq}）:")
            import json
            print(json.dumps(news_dict[sample_seq], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # 运行所有示例
    example_get_limit_up_news()
    example_get_limit_up_news_with_content()
    example_with_cookie()
    example_export_to_dict()

