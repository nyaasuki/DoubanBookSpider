import csv
import logging
import random
import time

from DoubanSpider.Spider import DoubanBook

if __name__ == '__main__':
    logger = logging.getLogger("PAPA")
    sleeptime = random.randint(0, 3)
    with open("results.csv", "a", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        writer.writerow(["书名", "作者", "上市时间", "价格", "评分", "书籍分类", "内容简介"])
    douban = DoubanBook()
    douban.main()
