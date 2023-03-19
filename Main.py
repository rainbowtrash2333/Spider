import Spider.qstheory as qs

if __name__ == "__main__":
    url = 'http://www.qstheory.cn/sitemap/'
    # url2 = 'http://www.qstheory.cn/ts/xstj/'
    qs.spider(url)
    qs.articles.wirte_to_csv()
