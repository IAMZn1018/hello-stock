"""
测试同花顺涨停雷达爬虫
"""
from app.utils.ths_crawler import THSCrawler


def test_basic_crawl():
    """基本爬取测试"""
    print("测试：爬取涨停雷达新闻")
    print("=" * 60)
    
    crawler = THSCrawler()
    news_list = crawler.get_limit_up_news()
    
    if news_list:
        print(f"✓ 成功获取 {len(news_list)} 条新闻\n")
        
        # 显示前 5 条
        for i, news in enumerate(news_list[:5], 1):
            print(f"{i}. [{news['time']}] {news['title']}")
            print(f"   data-seq: {news['data_seq']}")
            print(f"   URL: {news['url']}\n")
        
        if len(news_list) > 5:
            print(f"... 还有 {len(news_list) - 5} 条新闻")
    else:
        print("✗ 获取失败")


if __name__ == "__main__":
    test_basic_crawl()

