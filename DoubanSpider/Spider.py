from DoubanSpider import *
from DoubanSpider.db import Douban, engine, Recording
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("PAPA")
sleeptime = random.randint(0, 3)


class DoubanBook(object):
    def __init__(self):
        self.main_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
        self.base_url = 'https://book.douban.com/tag/{}'  # ?start={}&type=T
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
        """

        :param tag_name: 字符串格式 TAG名称
        :return:
        """
        for num in range(0, 10000, 20):
            time.sleep(sleeptime)
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
        response = requests.get(self.main_url, headers=self.headers)
        html = response.content.decode()
        tags = re.findall('.*?<a href="/tag/(.*?)">.*?</a>.*?', html)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        #     executor.map(self.get_url, [i for i in tags])
        for i in tags:
            print(f'[Spider]正在获取<{i}>链接数据.....')
            time.sleep(0.5)
            self.get_url(i)

    # def get_books_url(self, urls, tag_name):
    #     response = requests.get(url, headers=self.headers)
    #     html = response.content.decode()
    #     books_url = re.findall('.*?<a class="nbg" href="(.*?)".*?', html)
    #     self.get_data(books_url, tag_name)

    def get_data(self, row):
        """
        :param row: 数据库提取列表
        :return:  1.异常退出
        """
        time.sleep(sleeptime)
        print(f"正在解析：{row[0]}")
        response = requests.get(row[0], headers=self.headers)
        html = response.content.decode()
        try:
            name = re.findall('.*?<span property="v:itemreviewed">(.*?)</span>.*?', html)[0]
            author = re.findall('<meta name="keywords" content=".*?,(.*?),.*?', html)[0]
        except:
            logger.error(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]UNKNOWN URL:{row[0]}")
            return 1
        try:
            time_temp = re.findall('<span class="pl">出版年:</span> (.*?)<br/>.*?', html)[0]
        except:
            print(f'《{name}》未发现出版时间！')
            time_temp = 'N/A'
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
        data = [name, author, time_temp, price, score, row[1], intro]
        print(f'正在保存：{name}。')
        self.save_csv(data)
        rec = self.session.query(Recording).filter_by(id=1).scalar()
        rec.data = row[2]
        self.session.commit()

    @staticmethod
    def save_csv(data):
        """
        :param data: 数据
        :return:
        """
        with open('results.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
