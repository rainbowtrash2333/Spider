from urllib.parse import urlparse, urlunparse, urljoin, urlencode

# 假设爬取到的链接如下
link = "//example.com/path/to/page.html?foo=bar"

# 如果该链接缺少协议头，则使用 "http://" 添加协议头
if link.startswith("//"):
    link = "http:" + link

# 解析链接，得到其各个组成部分
parsed_link = urlparse(link)

# 如果该链接是相对路径，则使用当前页面的 URL 进行转换
if not parsed_link.scheme:
    base_url = "http://example.com/"
    link = urljoin(base_url, link)

# 对查询参数进行编码
query_params = {"baz": "qux"}
encoded_query_params = urlencode(query_params)

# 重新构造 URL
new_parsed_link = parsed_link._replace(query=encoded_query_params)
new_link = urlunparse(new_parsed_link)

print(new_link)