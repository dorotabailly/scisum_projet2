from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import pandas as pd
import unidecode as u


class StanfordScraper:

    def get_last_article(self):
        urls = self.get_articles_urls()
        content = self.parse_article(urls[0])
        return content
    
    def get_all_articles(self):
        """
        Scrap all articles from Stanford Newsletter

        Returns
        ---------
        articles: pandas.DataFrame
        """
        articles = pd.DataFrame(columns=["title", "date", "summary", "content"])
        for page_num in range(1,71):
            urls = scrap_stanford_articles_urls(self, page_num)
            for url in urls:
                content = self.parse_article(url)
                articles.append(content, ignore_index=True)
        return articles

    def get_articles_urls(self, page_num=1):
        url_news = f"https://news.stanford.edu/press-releases/page/{page_num}/"
        req = Request(url_news, headers={'User-Agent': 'Mozilla/5.0'})
        html_content=urlopen(req).read()
        soup = BeautifulSoup(html_content, features="html.parser")
        links = soup.find_all("a", attrs={"target":"press-release"})
        urls = [a["href"] for a in links]
        return urls

    def get_articles_urls_from_archive(self):
        years = range(1991, 2016)
        old_urls = []
        for year in years:
            url_news = f"https://news.stanford.edu/pr/{year}/"
            req = Request (url_news, headers={'User-Agent': 'Mozilla/5.0'})
            html_content=urlopen(req).read()
            soup = BeautifulSoup(html_content)
            links = soup.find_all("a", attrs={"target":"_blank"})
            old_urls.extend([a["href"] for a in links])
        return old_urls

    def parse_article(self, url):
        content = {}
        req = Request (url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content=urlopen(req).read()
        soup = BeautifulSoup(html_content, features="html.parser")
        titre = soup.find("h1")
        content["title"] = titre.text
        content["date"] = titre.find_previous("span").text
        content["summary"] = titre.find_next("div").text.strip()
        paragraphs = titre.find_next_siblings("p")
        contents = [p.text for p in paragraphs if "style" not in p.attrs]
        content["content"] = "\n".join(contents)
        content["url"] = url
        return content



class MaxPlanckScraper:

    def get_last_article(self):
        url = self.get_articles_urls(1, 1)[0]
        content = self.parse_article(url)
        return content

    def get_all_articles(self):
        """
        Scrap all articles from Max Plank Newsletter

        Returns
        ---------
        articles: pandas.DataFrame
        """
        articles_url = []
        for i in range(31):
            offset = i*100
            articles_url.extend(self.get_articles_urls(offset))
        
        articles = pd.DataFrame(columns=["title", "date", "summary", "content", "references", "tags"])
        for url_article in articles_url:
            content = self.parse_article(url_article)
            articles = articles.append(content, ignore_index=True)
        
        return articles


    
    def get_articles_urls(self, offset, articles_count=100):
        """ Retrieve articles urls from Max Planck newsletter
        for offset = 0 and articles_count = 100, the method returns the 100 first articles in the list.
        with an offset of 50 the method will return the [50-150] articles.

        Parameters
        --------
        offset: int
            Articles offset in Max Planck newsletters.
        articles_count: int
            Amount of articles retrieved.
        """
        articles_url = []
        url_news = f"https://www.mpg.de/newsroom_items/2249/more_items?category=&year=&context=news&limit={articles_count}&offset={offset}"
        html_content = requests.get(url_news).text
        
        soup = BeautifulSoup(html_content, features="html.parser")
        titles = soup.find_all("h3")
        
        root = "https://www.mpg.de"
        articles_url.extend([root+t.a["href"] for t in titles if t.a])
        return articles_url

    def parse_article(self, url_article):
        content={}
        html_content = requests.get(url_article).text
        soup = BeautifulSoup(html_content,features="html.parser")
        content["title"] = self.get_title(soup)
        content["date"] = self.get_date(soup)
        content["summary"] = self.get_summary(soup)
        content["content"] = self.get_article_content(soup)
        content["references"] = self.get_publications(soup)
        content["tags"] = self.get_article_tags(soup)
        content["url"] = url_article
        return content

    def get_title(self, soup):
        return soup.find("h1").text.strip()

    def get_date(self, soup):
        date = soup.find("span", class_="date")
        date = date.text.strip() if date else None
        return date

    def get_summary(self, soup):
        summary = soup.find(class_="summary")
        summary = summary.text.strip() if summary else None
        return summary

    def get_article_content(self, soup):
        article = soup.find("article")
        contents = article.find_all("div", class_="content")
        p_tags = contents[1].find_all("p", recursive=False)
        text = ' '.join( p.text.strip() for p in p_tags)
        return text

    def get_article_tags(self, soup):
        article = soup.find("article")
        meta_inf = article.find("div", class_="meta-information")
        tags = meta_inf.find("div", class_="tags")
        tags = tags.text.strip() if tags else None
        return tags
    
    def get_publications(self, soup):
        pubs = soup.find_all("div", class_="one_publication")
        clean_pubs = [ pub.text.strip() for pub in pubs ]
        clean_pubs = [u.unidecode(pub).replace('\n',' ') for pub in clean_pubs]
        return clean_pubs


if __name__ == "__main__":
    print(MaxPlanckScraper().get_last_article()["title"])
    print(StanfordScraper().get_last_article()["title"])