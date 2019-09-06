from DoubanSpider import *

try:
    import requests
    import re
    import time
    import csv

    print('支持库检查完成...')

except:
    print('正在安装支持库...')
    os.system('pip install SQLAlchemy')
    os.system('pip install csv')
    os.system('pip install requests')
    import requests
    import csv


class DoubanBook(object):
    def __init__(self):
        self.main_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        self.base_url = 'https://book.douban.com/tag/{}'  # ?start={}&type=T
        self._lock = threading.Lock()
        self.headers = {
            'DNT': '1',
            'Host': 'book.douban.com',
            'Referer': 'https://book.douban.com/',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

    def get_url(self, tag_name):
        for num in range(0, 1000, 20):
            url = self.base_url.format(tag_name) + f'?start={num}&type=T'
            print(f"正在获取{tag_name}分类下的书籍...当前页码:{num / 20 + 1}")
            try:
                response = requests.get(url, headers=self.headers)
                html = response.content.decode()
                books_url = re.findall('.*?<a class="nbg" href="(.*?)".*?', html)
                print(books_url)
                self.get_data(books_url, tag_name)
            except:
                break

    def get_tags(self):
        print('开始获取tags。')
        response = requests.get(self.main_url, headers=self.headers)
        html = response.content.decode()
        tags = re.findall('.*?<a href="/tag/(.*?)">.*?</a>.*?', html)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     executor.map(self.get_url, [i for i in tags])
        for i in tags:
            self.get_url(i)

    # def get_books_url(self, urls, tag_name):
    #     response = requests.get(url, headers=self.headers)
    #     html = response.content.decode()
    #     books_url = re.findall('.*?<a class="nbg" href="(.*?)".*?', html)
    #     self.get_data(books_url, tag_name)

    def get_data(self, urls, tag_name):
        for url in urls:
            print(f"正在解析：{url}")
            response = requests.get(url, headers=self.headers)
            html = response.content.decode()
            name = re.findall('.*?<span property="v:itemreviewed">(.*?)</span>.*?', html)[0]
            author = re.findall('<meta name="keywords" content=".*?,(.*?),.*?', html)[0]
            time = re.findall('<span class="pl">出版年:</span> (.*?)<br/>.*?', html)[0]
            price = re.findall('<span class="pl">定价:</span> (.*?)<br/>.*?', html)[0]
            score = re.findall('<strong class="ll rating_num " property="v:average">(.*?)</strong>.*?', html)[0]
            intro = re.findall('内容简介[\\s\\S]*?<div class="intro">([\\s\\S]*?)</div>', html)[0]
            intro = (re.sub('\s', '', intro)).replace('<p>', '').replace('</p>', ' ')
            data = [name, author, time, price, score, tag_name, intro]
            print(f'正在保存：{name}。')
            self.save_csv(data)

    def save_csv(self, data):
        with open('results.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def main(self):
        with open("results.csv", "w", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["书名", "作者", "上市时间", "价格", "评分", "书籍分类", '内容简介'])
        self.get_tags()


if __name__ == '__main__':
    douban = DoubanBook()
    douban.main()
