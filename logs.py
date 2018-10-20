import psycopg2

CONNECT_STRING = "dbname=news"

ARTICLES_QUERY = """
SELECT title, count(*) as article_views FROM articles
JOIN log ON articles.slug = substring(log.path, 10)
GROUP BY title ORDER BY article_views DESC LIMIT 3;
"""

AUTHORS_QUERY = """
SELECT authors.name, count(*) as author_views FROM articles
JOIN authors ON articles.author = authors.id
JOIN log ON articles.slug = substring(log.path, 10)
WHERE log.status LIKE '200 OK' GROUP BY authors.name ORDER BY author_views DESC;
"""


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Log(object):
    def __init__(self):
        self.db = psycopg2.connect(CONNECT_STRING)
        self.c = self.db.cursor()

    def get_articles(self):
        self.c.execute(ARTICLES_QUERY)
        articles = self.c.fetchall()
        print(Color.PURPLE + "The three most popular articles" + Color.END)
        for article in articles:
            print('"{0}" — {1} views'.format(*article))
        print()

    def get_authors(self):
        self.c.execute(AUTHORS_QUERY)
        authors = self.c.fetchall()
        print(Color.DARKCYAN + "The most popular article authors" + Color.END)
        for author in authors:
            print('"{0}" — {1} views'.format(*author))
        print()

    def print_log(self):
        self.get_articles()
        self.get_authors()


if __name__ == '__main__':
    log = Log()
    print(Color.BOLD + 'Log Analysis' + Color.END)
    print(Color.UNDERLINE + '            ' + Color.END)
    log.print_log()
