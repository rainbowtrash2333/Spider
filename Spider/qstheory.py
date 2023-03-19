import urllib3
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import urlparse, urljoin
from Been.ArticlesData import ArticlesData

sys.path.append(r'..')
from Been.Article import Article

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': ' gzip, deflate',
    'Accept-Language': ' zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
    'Cache-Control': ' max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=183bfcc170c53e-0c8851da5dbd7b-7b555472-144000-183bfcc170d7c3; '
              'CNZZDATA30019853=cnzz_eid%3D386557323-1665369225-null%26ntime%3D1665369225; wdcid=709e53b6bc225834; '
              'wdlast=1677468859',
    'Host': 'www.qstheory.cn',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/111.0.0.0',
}

http = urllib3.PoolManager()
a_set = set()
articles = ArticlesData()
url_pattern_string = "^http(S)?:\\/\\/(?:www\\.)?(qstheory)\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
web_root = 'http://www.qstheory.cn'


def is_url(string):
    url_pattern = re.compile(url_pattern_string)
    return bool(url_pattern.match(string))


def get_HTML(url='http://www.qstheory.cn/sitemap'):
    if is_url(url):
        try:
            r = http.request('GET', url, headers=headers, timeout=3)
            if r.status == 200:
                return r.data
            else:
                return "<html></html>"
        except TimeoutError:
            print("链接超时：" + url)
            return "<html></html>"


def is_article(soup):
    return len(soup.find_all(attrs={"class": 'pubtime'})) != 0 and len(soup.find_all('h1')) != 0


def spider(current_url):
    current_url = current_url.rstrip("/")
    print(current_url)
    # 添加进a_set,代表处理过的a标签
    if current_url in a_set:
        print("重复 " + current_url)
        return 0
    a_set.add(current_url)
    soup = BeautifulSoup(get_HTML(current_url), 'lxml')
    # 是文章就抓取内容
    # 不是文章就找到所有链接，然后递归抓取
    if is_article(soup):
        articles.add(get_article(soup, current_url))
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
            elif not is_url(url):
                continue
            if not urlparse(url).scheme:
                url = urljoin(current_url, url)

            spider(url)


def get_article(soup, url):
    author = ''
    source = ''
    content = ''
    if not is_article(soup):
        return 0
    title = soup.find('h1').string
    publish_date = soup.find(attrs={"class": 'pubtime'}).string

    foo = soup.find(attrs={"class": 'appellation'}, string=re.compile("作者"))
    if foo is not None:
        author = soup.find(attrs={"class": 'appellation'},
                           string=re.compile("作者")).string[6:]
    foo = soup.find(attrs={"class": 'appellation'}, string=re.compile("来源"))
    if foo is not None:
        source = soup.find(attrs={"class": 'appellation'},
                           string=re.compile("来源")).string[6:]

    for p in soup.find_all('p', string=re.compile("[\u4e00-\u9fa5]+[，。？！；“”》】}]")):
        if p.string is not None:
            content = content + '\n' + p.string
    return Article(url=url, title=title, content=content, publish_date=publish_date, author=author, source=source)


if __name__ == "__main__":
    url1 = 'http://www.qstheory.cn/sitemap'
    url2 = 'http://www.qstheory.cn/2023-03/13/c_1129426852.htm'
    spider(url1)
