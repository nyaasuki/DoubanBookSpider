from DoubanSpider import *
from DoubanSpider.db import Douban, engine
from sqlalchemy.orm import sessionmaker


class DoubanBook(object):
    def __init__(self):
        self.main_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        self.base_url = 'https://book.douban.com/tag/{}'  # ?start={}&type=T
        self._lock = threading.Lock()
        self.session = sessionmaker(engine)()
        self.headers = {
            'Referer': 'https://www.baidu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.132 Safari/537.36 '
        }
        self.log = logging.basicConfig(filename='papa.log',
                                       filemode='a',
                                       format='%(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

    def get_url(self, tag_name):
        for num in range(0, 10000, 20):
            url = self.base_url.format(tag_name) + f'?start={num}&type=T'
            print(f'正在获取 TAG：<{tag_name}> 书籍信息', num)
            response = requests.get(url, headers=self.headers)
            html = response.content.decode()
            books_url = re.findall('.*?<a class="nbg" href="(.*?)".*?', html)
            if not books_url:
                break
            for i in books_url:
                try:
                    self.session.add(Douban(tag=tag_name, url=i))
                    self.session.commit()
                except:
                    self.session.rollback()

    def get_tags(self):
        print('[SQL]未发现TAGS数据！')
        print('[Spider]正在准备TAG数据，这需要一定时间.....')
        do_not_get_all = input('[Spider]请选择运行模式：\n1.获取所有TAG（需要大量时间）\n2.获取单一TAG\n请输入对应数字，回车确定\n')
        if do_not_get_all == '1':
            response = requests.get(self.main_url, headers=self.headers)
            html = response.content.decode()
            tags = re.findall('.*?<a href="/tag/(.*?)">.*?</a>.*?', html)
            # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            #     executor.map(self.get_url, [i for i in tags])
            for i in tags:
                print(f'[Spider]正在获取<{i}>链接数据.....')
                self.get_url(i)
        elif do_not_get_all == '2':
            user_tag = input('请输入标签：')
            self.get_url(user_tag)
            self.main()
        else:
            print("[Spider]输入有误，请重新输入！")
            self.get_tags()
        self.get_data()

    # def get_books_url(self, urls, tag_name):
    #     response = requests.get(url, headers=self.headers)
    #     html = response.content.decode()
    #     books_url = re.findall('.*?<a class="nbg" href="(.*?)".*?', html)
    #     self.get_data(books_url, tag_name)

    def get_data(self):
        for row in self.session.query(Douban.url, Douban.tag).all():
            print(f"正在解析：{row[0]}")
            response = requests.get(row[0], headers=self.headers)
            html = response.content.decode()
            try:
                name = re.findall('.*?<span property="v:itemreviewed">(.*?)</span>.*?', html)[0]
                author = re.findall('<meta name="keywords" content=".*?,(.*?),.*?', html)[0]
            except:
                logger.error(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]UNKNOWN URL:{row[0]}")
                continue
            try:
                time = re.findall('<span class="pl">出版年:</span> (.*?)<br/>.*?', html)[0]
            except:
                print(f'《{name}》未发现出版时间！')
                time = 'N/A'
                logger.warning(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]CAN'T GET TITLE <time>:{row[0]}")
            try:
                price = re.findall('<span class="pl">定价:</span> (.*?)<br/>.*?', html)[0]
            except:
                logger.warning(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]CAN'T GET TITLE <price>:{row[0]}")
                print(f'《{name}》未发现定价！')
                price = 'N/A'
            try:
                score = re.findall('<strong class="ll rating_num " property="v:average">(.*?)</strong>.*?', html)[0]
            except:
                logger.warning(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]CAN'T GET TITLE <score>:{row[0]}")
                print(f'《{name}》未发现评分！')
                score = 'N/A'
            try:
                intro = re.findall('内容简介[\\s\\S]*?<div class="intro">([\\s\\S]*?)</div>', html)[0]
                intro = (re.sub('\s', '', intro)).replace('<p>', '').replace('</p>', ' ')
            except:
                logger.warning(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]CAN'T GET TITLE <intro>:{row[0]}")
                print(f'《{name}》未发现简介！')
                intro = '无'
            data = [name, author, time, price, score, row[1], intro]
            print(f'正在保存：{name}。')
            self.save_csv(data)

    def save_csv(self, data):
        with open('results.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def main(self):
        n = self.session.query(Douban.url, Douban.tag).all()
        if not n:
            self.get_tags()
        else:
            print('[Spider]检测到现有TAG数据，开始抓取...')
            self.get_data()


if __name__ == '__main__':
    logger = logging.getLogger("PAPA")
    with open("results.csv", "a", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        writer.writerow(["书名", "作者", "上市时间", "价格", "评分", "书籍分类", "内容简介"])
    douban = DoubanBook()
    douban.main()
