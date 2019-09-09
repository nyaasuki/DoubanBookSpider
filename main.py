import csv
import logging
import random
import time
from cmd import Cmd

from DoubanSpider.db import Douban
from DoubanSpider.Spider import DoubanBook


class SpiderMain(Cmd):
    def __init__(self):
        super().__init__()
        pass

    def do_help(self, arg):
        pass

    def do_start(self, arg):
        pass

    def do_tag(self,arg):
        pass

def url_pool():
    for row in douban.session.query(Douban.url, Douban.tag).all():
        yield row


if __name__ == '__main__':
    sleeptime = random.randint(0, 3)
    with open("results.csv", "a", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        writer.writerow(["书名", "作者", "上市时间", "价格", "评分", "书籍分类", "内容简介"])
    douban = DoubanBook()
    douban.main()
