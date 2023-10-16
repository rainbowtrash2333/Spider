import urllib3
import re
from Been.ArticlesData import ArticlesData
from abc import ABCMeta, abstractmethod
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


class Spider(metaclass=ABCMeta):
    def __init__(self, headers, url, url_pattern=r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'):
        self.url = url
        self.headers = headers
        self.url_pattern_string = url_pattern
        self.http = urllib3.PoolManager()
        self.a_set = set()
        self.articles = ArticlesData()

    def is_url(self, string):
        url_pattern = re.compile(self.url_pattern_string)
        return bool(url_pattern.match(string))

    def get_HTML(self, url):
        if self.is_url(url):
            try:
                r = self.http.request('GET', url, headers=self.headers, timeout=3)
                if r.status == 200:
                    return r.data
                else:
                    return "<html></html>"
            except TimeoutError:
                print("链接超时：" + url)
                return "<html></html>"

    @abstractmethod
    def is_article(soup):
        pass

    # 递归爬取所有的a标签
    def spider(self, current_url=None):
        if current_url is None:
            current_url = self.url
        current_url = current_url.rstrip("/")
        print(current_url)
        # 添加进a_set,代表处理过的a标签
        if current_url in self.a_set:
            print("重复 " + current_url)
            return 0
        self.a_set.add(current_url)
        soup = BeautifulSoup(self.get_HTML(current_url), 'lxml')
        # 是文章就抓取内容
        # 不是文章就找到所有链接，然后递归抓取
        if self.is_article(soup):
            self.articles.add(self.get_article(soup, current_url))
        else:
            for a in soup.find_all('a'):
                # a 标签没有href
                # href为空
                # href 为锚定
                # href 为js
                # href 为相对、绝对路径
                if 'href' not in a.attrs:
                    continue
                elif a['href'] is None:
                    continue
                url = a['href'].strip()
                if url == '':
                    continue
                elif url.startswith('#'):
                    continue
                elif url.startswith('javascript:'):
                    continue
                elif not self.is_url(url):
                    continue
                if not urlparse(url).scheme:
                    url = urljoin(current_url, url)
                self.spider(url)

    @abstractmethod
    def get_article(self):
        pass
