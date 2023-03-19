import pandas as pd


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
        self.data['content'].append(article.content)
        self.data['publish_date'].append(article.publish_date)
        self.data['author'].append(article.author)
        self.data['source'].append(article.source)

    def wirte_to_csv(self, path='./data.csv'):
        df = pd.DataFrame(self.data)
        df = df.set_index('url')
        print(df)
        df.to_csv(path)
