class Article:
    def __init__(self, url, title, content, publish_date, author, source):
        self.url = url
        self.title = title
        self.content = content
        self.publish_date = publish_date
        self.author = author
        self.source = source

    def __list__(self):
        return [self.url, self.title, self.content, self.author, self.source, self.publish_date]

    def __dict__(self):
        return {
            'url': self.url,
            'title': self.title,
            'publish_date': self.publish_date,
            'author': self.author,
            'content': self.content,
            'source': self.source,
        }


class ArticlesData:

    def __init__(self):
        self.data = {
            'url': [],
            'title': [],
            'publish_date': [],
            'author': [],
            'content': [],
            'source': [],
        }

    def add(self, article):
        self.data['url'].append(article.url)
        self.data['title'].append(article.title)
        self.data['publish_date'].append(article.publish_date)
        self.data['author'].append(article.author)
        self.data['source'].append(article.source)
